import sys
import re
import sqlalchemy
from sqlalchemy import exists, and_
from sqlalchemy.orm import joinedload, load_only, selectinload
from db_models import session, engine, metadata, Contact, Phone


EXIT_COMMANDS = ('good bye', 'close', 'exit', '.')


def add_phone(data):
    name, phone = data

    result_name = session.query(Contact).filter(
        Contact.contact_name == name).first()

    result_phone = session.query(Phone).filter(Phone.phone == phone).first()

    if result_name and result_phone:
        info = '\n\tEntered contact with phone already exist'
    else:
        try:
            new_contact_name = Contact(
                contact_name=name
            )
            session.add(new_contact_name)
            session.commit()

            new_contact_phone = Phone(
                phone=phone, contact_id=new_contact_name.id
            )
            session.add(new_contact_phone)
            session.commit()

            info = '\n\tContact has been successfully added to addressbook'
        except Exception as e:
            print(e)
            info = '\n\tCheck entered data.'

    return info


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
        r'\badd\b|\bdelete\b|\bphone\b|\bshow\s{1}all\b|\bgood\s{1}bye\b|\bclose\b|\bexit\b|[.]{1}', string)
    command = raw_user_input.group() if raw_user_input else False

    # parsing for assigning phone number
    raw_phone = re.search(
        r'38(097|098|096|068|067|063|068|099)\d{7}', string)
    phone = raw_phone.group() if raw_phone else False

    # parsing for assigning name
    raw_name = re.search(
        r'(?!.*(add|delete|phone|show|all|good|bye|close|exit|\.{1})+)\s[a-zA-Z]+\s{1}[a-zA-Z]+', string)
    name = raw_name.group().strip().title() if raw_name else False

    data = (name, phone)

    return command, data


def show_all_contacts():
    result = session.query(Contact.id, Contact.contact_name,
                           Phone.phone).join(Phone).all()
    output = ''
    for el in result:
        output += f'\t{el[1]} - {el[-1]}\n'
    return output


def show_one_contact_data(data):
    name, _ = data
    result = session.query(Contact.id, Contact.contact_name,
                           Phone.phone).join(Phone).filter(Contact.contact_name == name).all()
    if result:
        output = ''
        for el in result:
            output += f'\t{el[1]} - {el[-1]}\n'
    else:
        output = '\tThere is not such contact.'
    return output


def delete_contact(data):
    name, _ = data
    result = session.query(Contact).filter(Contact.contact_name == name).all()

    if result:

        for _ in range(len(result)):

            result = session.query(Contact).filter(
                Contact.contact_name == name).first()
            id = result.id

            if result:
                result = session.query(Contact).get(id)
                session.delete(result)
                session.commit()

        output = f'\tAll info for contact {name} were deleted'

    else:
        output = '\tThere is not such contact.'

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

    To exit enter one of the following commands:
        <good bye>, <close>, <exit>, <.>
    '''
    )

    while True:

        user_command = input('\nWaitting for your comand: ')
        user_command = user_command.casefold()

        command, data = parsing_user_input(user_command)

        info = handler_func(command, data)
        print('=' * 75)
        print(info)


if __name__ == '__main__':
    main()
