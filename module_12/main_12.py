from funcs_12 import *
from pathlib import Path
import sys

EXIT_COMMANDS = ('good bye', 'close', 'exit', '.')


def inner_parser(data):
    name, phone = data
    name = Name(name).name
    phone = Phone(phone).phone
    return name, phone

# add phone number


def add_phone(address_book, data):
    name, phone = inner_parser(data)
    if name not in address_book:
        record = Record()
        record.add_contact_phonenumb(phone)
        user_input = input(
            f'\n\tDo you want to enter birthday for contact <{name}>? \n\tEnter y|n:').casefold()
        if user_input == 'y':
            raw_birthday = input(
                '\n\tEnter contact\'s birthday in format <dd.mm.yyyy>: ')
            record.birthday = raw_birthday
        birthday_info = record.days_to_birthday()
        print(birthday_info)
        address_book.add_record(name, record.__dict__)
        result = f'\n\tThe contact <{name}> was added to address book with phone <{phone}>.'

    elif name in address_book and phone in address_book[name]['phones']:
        result = f'\n\tThe contact\'s data is already in address book.'
    elif name in address_book and phone not in address_book[name]['phones']:
        address_book[name]['phones'].append(phone)
        result = f'\n\tThe phone <{phone}> for contact <{name}>\n\twas successfully added to address book.'
    else:
        raise ValueError
    return result


def change_existing_phone(address_book, data):
    name, phone = inner_parser(data)
    if name in address_book and phone in address_book[name]['phones']:
        old_phone = phone
        new_phone = input(f'\n\tEnter new phone for contact <{name}>: ')
        raw_phone = re.search(
            r'38(097|098|068|067|063|068|099)\d{7}', new_phone)
        phone = raw_phone.group().strip() if raw_phone else False
        if phone:
            address_book[name]['phones'].remove(old_phone)
            phone = Phone(phone).phone
            address_book[name]['phones'].append(phone)
            return f'\n\tPhone number <{old_phone}> for contact <{name}>\n\twas successfully changed for <{phone}>.'
    elif (name not in address_book or phone not in address_book[name]['phones']) \
            or (name not in address_book and phone not in address_book[name]['phones']):
        raise ValueError


def deserialize_data(file_name):
    with open(file_name, 'rb') as fh:
        result = pickle.load(fh)
    return result


def save_and_exit(address_book):
    path = Path('data.bin')
    serialize_data(address_book, path)
    sys.exit(f'\n\tThe address book was saved to <{path}> file.\n\tGood bye!')


def serialize_data(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except StopIteration:
            ex_info = f'\n\tYou have seem all contact\'s info.'
        except Exception as ex:
            ex_info = ex  # f'\n\tEnter correct data, please.'
        return ex_info
    return wrapper


def parsing_user_input(string):
    """
    Function takes some string and separates one in three values

    Takes one parametr namely string from user input. Returns tuple with
    three values init or False if no value.
    """

    # parsing for assigning comand
    raw_user_input = re.search(
        r'\badd\b|\bchange\b|\bphones\b|\bshow\s{1}all\b|\bgood\s{1}bye\b|\bclose\b|\bexit\b|[.]{1}', string)
    command = raw_user_input.group() if raw_user_input else False

    # parsing for assigning phone number
    raw_phone = re.search(
        r'38(097|098|068|067|063|068|099)\d{7}', string)
    phone = raw_phone.group() if raw_phone else False

    # parsing for assigning name
    raw_name = re.search(
        r'(?!.*(add|change|phones|good|bye|close|exit|\.{1})+)\s[a-zA-Z]+\s{1}[a-zA-Z]+', string)
    name = raw_name.group().strip().title() if raw_name else False

    data = (name, phone)

    return command, data

# use iterator


def show_all_contacts(address_book):
    print(f'\n\tAddress book has <{len(address_book)}> contacts.')
    n = int(input(f'\n\tEnter how many rows you preffer to see: '))
    info = address_book.iterator(n)
    while True:
        print(next(info))
        user_input = input('\n\tDo you want to prosside y|n: ').casefold()
        if user_input == 'y':
            continue
        elif user_input == 'n':
            return f'\n\tContinue your work with commands.'


def show_one_contact_data(address_book):
    user_input = input(
        '\n\tEnter part of contact full name or phone number: ').casefold()
    return address_book.search_contacts(user_input)


@input_error
def handler_func(command, address_book, data):
    if command in COMMANDS:
        if command in ['show all', 'good bye', 'close', 'exit', '.', 'phones']:
            result = COMMANDS[command](address_book)
        else:
            result = COMMANDS[command](address_book, data)
        return result
    else:
        raise ValueError


COMMANDS = {
    'add': add_phone,
    'show all': show_all_contacts,
    'good bye': save_and_exit,
    'close': save_and_exit,
    'exit': save_and_exit,
    '.': save_and_exit,
    'change': change_existing_phone,
    'phones': show_one_contact_data
}


def main():
    print(
        '''
    WORKING INSTRUCTION

    To continue working you have following commands:
        Enter <hello> - to load address book.

    After entering initial comand you have following commands:

        <add name surname phone number> BLANK SIGNS REQUIRED
        (format example - add Name Surname 38XXXXXXXXXX),

        <change name surname phone number> BLANK SIGNS REQUIRED
        (format example - change Name Surname 38XXXXXXXXXX),
     
        <phones name surname> BLANK SIGNS REQUIRED
        (format example - phones Name Surname),

    To exit enter one of the following commands:
        <good bye>, <close>, <exit>, <.>

    To show phon book enter <show all>
    '''
    )

    initial_user_comand = input('\n\tWaitting for your comand: ').casefold()

    while not initial_user_comand == 'hello':
        print(f'\n\tIn order to work with address book enter <Hello>')
        initial_user_comand = input(
            '\n\tWaitting for your comand: ').casefold()

    path = Path('data.bin')
    path_exists = path.is_file()

    address_book = deserialize_data(
        path) if path_exists else AddressBook()

    if path_exists:
        print(
            f'\n\tYou address book has been restored from <{path}> file,\n\tand it\'s ready to work.')

    else:
        print(f'\n\tCongratulation, you have created new address book!')

    while True:

        user_command = input('\nWaitting for your comand: ')
        user_command = user_command.casefold()

        command, data = parsing_user_input(user_command)
        print(command, data)

        info = handler_func(command, address_book, data)
        print(info)


if __name__ == '__main__':
    main()
