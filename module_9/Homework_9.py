import re

phone_book = {}

EXIT_COMMANDS = ('good bye', 'close', 'exit', '.')


def add_new_contact_func(name, phone_number):
    """
    Function adds new contact and phone number to phone book.

    Takes to parameters namely contact name and contact's phone number.
    """

    if name in phone_book:
        result = f'\n\tContact <{name}> already exists\n'
        return result

    elif not name == False and not phone_number == False:
        phone_book[name] = phone_number
        result = f'\n\tNew contact <{name}> with phone number <{phone_number}> has been saved successfully\n'
        return result

    else:
        raise ValueError


def change_phone_numb_func(name, phone_number):
    """
    Function changes existing phone number for particular contact. 

    Takes to parameters namely contact name and contact's phone number.
    """

    if name in phone_book and phone_number != False:
        phone_book[name] = phone_number
        return f'\n\tFor contact <{name}> was set new phone number <{phone_number}>\n'
    elif name == False or phone_number == False:
        raise ValueError
    else:
        return f'\n\tThere is no such contact <{name}> in phone book. Add contact as new one\n'


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except KeyError as ex:
            ex_info = f'\n\tEnter correct command, please.'
        except ValueError as ex:
            ex_info = f'\n\tGive me correct name or/and phone number.'
        except IndexError as ex:
            ex_info = f'\n\tEnter correct data, please.'
        return ex_info
    return wrapper


def show_user_phone_func(name):
    """
    Function shows phone number for existing contact.

    Takes one parametr namely contact name.
    """

    if name in phone_book:
        contact_phonenumb = phone_book[name]
        return f'\n\tContant <{name}> has following phone number <{contact_phonenumb}>'
    elif name not in phone_book and name != False:
        return f'\n\tThere is no contact <{name}> in phone book'
    elif name == False:
        raise ValueError


def parsing_user_input(string):
    """
    Function takes some string and separates one in three values.py

    Takes one parametr namely string from user input. Returns tuple with
    three values init or False if no value.
    """

    # parsing for assigning comand
    raw_user_input = re.search(r'(?:^add\b|^change\b|^phone\b)', string)
    command = raw_user_input.group() if raw_user_input else False

    # parsing for assigning phone number
    phone_number = ''.join(re.findall('\d+', string))
    if len(phone_number) == 12:
        phone_number = f'+{phone_number}'
    elif len(phone_number) == 10:
        phone_number = f'+38{phone_number}'
    else:
        phone_number = False

    # parsing for assigning name
    clear_name = re.search(
        r'[^(?:^add\b|^change\b|^phone\b)][a-zA-Z]+\s{1}[a-zA-Z]+', string)
    name = clear_name.group().strip().title() if clear_name else False

    return command, phone_number, name


@input_error
def handler_func(command, name, phone_number):
    if command == 'add' or command == 'change':
        result = COMMANDS[command](name, phone_number)
    else:
        result = COMMANDS[command](name)
    return result


def main():
    print(
        '''
    WORKING INSTRUCTION

    To continue working you have following commands:
        <hello>,

        <add name surname phone number> BLANK SIGNS REQUIRED
        (format example - 0685119811/380685119811),

        <change name surname phone number> BLANK SIGNS REQUIRED
        (format example - 0685119811/380685119811),

        <phone name surname> BLANK SIGNS REQUIRED

    To exit enter one of the following commands:
        <good bye>, <close>, <exit>, <.>

    To show phon book enter <show all>
    '''
    )

    while True:

        user_command = input('\nWaitting for your comand: ')
        user_command = user_command.casefold()

        if user_command in EXIT_COMMANDS:
            print('\n\tGood bye!\n')
            break

        elif user_command == 'show all':
            for k, v in phone_book.items():
                print(f'\tContact <{k}> has following phone number <{v}>')

        elif user_command == 'hello':
            print('\n\tHow could I help you?\n')

        else:
            command, phone_number, name = parsing_user_input(user_command)
            print(handler_func(command, name, phone_number))


COMMANDS = {
    'add': add_new_contact_func,
    'change': change_phone_numb_func,
    'phone': show_user_phone_func
}

if __name__ == '__main__':
    main()
