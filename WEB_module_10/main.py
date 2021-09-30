import sys
import re
from lru_cash import lru_cash, red
from mongo_conf import assistant


EXIT_COMMANDS = ('good bye', 'close', 'exit', '.')


# HW_10 DONE
def add_phone(data):
    name, phone = data
    contact_counter = assistant.count_documents(
        {"name": name, "phone": phone})

    print(f'\n\t{contact_counter}')

    if contact_counter == 0:
        assistant.insert_one({"name": name, "phone": phone})
        output = '\n\tContact has been successfully added to addressbook'
    else:
        output = f'\n\tEntered contact with phone {phone} already exist'

    return output


def save_and_exit():
    sys.exit(f'\n\tThe address book was saved.\n\tGood bye!')


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except StopIteration:
            ex_info = f'\n\tYou have seem all contact\'s info.'
        except Exception as ex:
            ex_info = ex
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
        r'\badd\b|\bchange\b|\bdelete\b|\bphone\b|\bshow\s{1}all\b|\bgood\s{1}bye\b|\bclose\b|\bexit\b|[.]{1}', string)
    command = raw_user_input.group() if raw_user_input else False

    # parsing for assigning phone number
    raw_phone = re.search(
        r'38(097|098|096|068|067|063|068|099)\d{7}', string)
    phone = raw_phone.group() if raw_phone else False

    # parsing for assigning name
    raw_name = re.search(
        r'(?!.*(add|delete|change|phone|show|all|good|bye|close|exit|\.{1})+)\s[a-zA-Z]+\s{1}[a-zA-Z]+', string)
    name = raw_name.group().strip().title() if raw_name else False

    data = (name, phone)

    return command, data


# HW_10 DONE
def show_all_contacts():

    output = ''

    result = assistant.find({})
    for el in result:
        name = el['name']
        phone = el['phone']
        output += f'\t{name} - {phone}\n'

    return output


# DONE
@lru_cash(red)
def show_one_contact_data(data):
    name, phone = data

    contact_counter = assistant.count_documents(
        {"name": name})

    if contact_counter > 0:
        result = assistant.find({'name': name})
        output = ''
        for el in result:
            name = el['name']
            phone = el['phone']
            output += f'\t{name} - {phone}\n'
    else:
        output = '\tThere is not such contact.'

    return output


def delete_contact(data):
    name, phone = data
    if not phone:
        assistant.delete_many({"name": name})
        output = f'\n\tAll data for contact {name} were deleted.'
    elif phone and name:
        assistant.delete_one({'name': name, 'phone': phone})
        output = f'\n\tPhone {phone} for contact {name} was deleted.'
    else:
        output = f'\n\tEnter correct data.'

    return output


def change_phone(data):
    name, phone = data

    contact_counter = assistant.count_documents(
        {"name": name})

    if contact_counter > 0:
        output = delete_contact(data)
    else:
        output = '\n\tThere is not such contact.'
    print(output)

    new_phone = input('\n\tEnter new contact phone number: ')

    raw_phone = re.search(
        r'38(097|098|096|068|067|063|068|099)\d{7}', new_phone)
    new_phone = raw_phone.group() if raw_phone else False

    if new_phone:
        new_data = name, new_phone
        add_phone(new_data)
        output = '\n\tContact were changed successfully.'
    else:
        output = '\n\tInvalid phone format. Repeat command.'

    return output


@input_error
def handler_func(command, data):

    if command in COMMANDS:
        if command in ['show all', 'good bye', 'close', 'exit', '.', 'phones']:
            result = COMMANDS[command]()
        else:
            result = COMMANDS[command](data)
        return result
    else:
        raise ValueError


COMMANDS = {
    'add': add_phone,
    'show all': show_all_contacts,
    'phone': show_one_contact_data,
    'change': change_phone,
    'delete': delete_contact,
    'good bye': save_and_exit,
    'close': save_and_exit,
    'exit': save_and_exit,
    '.': save_and_exit
}


def main():
    print(
        '''
    You have following commands:

        <add Name phone number> BLANK SIGNS REQUIRED
        (format example - add Name 38XXXXXXXXXX),

        <show all> BLANK SIGNS REQUIRED
        (format example - show all),

        <phone Name> BLANK SIGNS REQUIRED
        (format example - phone Name),

        <delete Name> BLANK SIGNS REQUIRED
        (format example - delete Name)

        <change Name phone number> BLANK SIGNS REQUIRED
        (format example - change Name 38XXXXXXXXXX),

    To exit enter one of the following commands:
        <good bye>, <close>, <exit>, <.>
    '''
    )

    while True:

        user_command = input('\nWaitting for your comand: ')
        user_command = user_command.casefold()

        command, data = parsing_user_input(user_command)

        info = handler_func(command, data)
        print('=' * 80)
        print(info)


if __name__ == '__main__':
    main()
