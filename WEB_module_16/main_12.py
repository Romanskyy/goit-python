"""Personal assistant main module

The script allows to use extrafunctions for
classes collected in funcs.py module
"""

import sys
import re
import pickle
from pathlib import Path
from funcs_12 import Phone, Name, Record, AddressBook


EXIT_COMMANDS = ("good bye", "close", "exit", ".")


def inner_parser(data):
    """Returns cleared phone and name

    Parameters
    ----------
    data : tuple

    Returns
    -------
    name -> instance of class Name
    phone -> instance of class Phone
    """
    name, phone = data
    name = Name(name).name
    phone = Phone(phone).phone
    return name, phone


def add_phone(address_book, data):
    """Add phone to addressbook or
    creates phone if not exists

    Parameters
    ----------
    data : tuple

    Returns
    -------
    Info-string about condition anter function has worked
    """
    name, phone = inner_parser(data)
    if name not in address_book:
        record = Record()
        record.add_contact_phonenumb(phone)
        user_input = input(
            f"\n\tDo you want to enter birthday for contact <{name}>? \n\tEnter y|n:"
        ).casefold()
        if user_input == "y":
            raw_birthday = input(
                "\n\tEnter contact's birthday in format <dd.mm.yyyy>: "
            )
            record.birthday = raw_birthday
        birthday_info = record.days_to_birthday()
        print(birthday_info)
        address_book.add_record(name, record.__dict__)
        result = (
            f"\n\tThe contact <{name}> was added to address book with phone <{phone}>."
        )

    elif name in address_book and phone in address_book[name]["phones"]:
        result = "\n\tThe contact's data is already in address book."
    elif name in address_book and phone not in address_book[name]["phones"]:
        address_book[name]["phones"].append(phone)
        result = f"\n\tThe phone <{phone}> for contact <{name}>\n\t\
        was successfully added to address book."
    else:
        raise ValueError
    return result


def change_existing_phone(address_book, data):
    """Changs existiong phone in address book

    Parameters
    ----------
    address_book: dict
    data: tuple

    Returns
    -------
    Info-string about condition anter function has worked
    """
    name, phone = inner_parser(data)
    if name in address_book and phone in address_book[name]["phones"]:
        old_phone = phone
        new_phone = input(f"\n\tEnter new phone for contact <{name}>: ")
        raw_phone = re.search(r"38(097|098|068|067|063|068|099)\d{7}", new_phone)
        phone = raw_phone.group().strip() if raw_phone else False
        if phone:
            address_book[name]["phones"].remove(old_phone)
            phone = Phone(phone).phone
            address_book[name]["phones"].append(phone)
            result = f"\n\tPhone number <{old_phone}> for contact <{name}>\n\t\
            was successfully changed for <{phone}>."
    return result or ValueError


def deserialize_data(file_name):
    """Deserializes data from the file shown

    Parameters
    ----------
    file_name : file

    Returns
    -------
    result: deserialized file
    """
    with open(file_name, "rb") as f_h:
        result = pickle.load(f_h)
    return result


def save_and_exit(address_book):
    """Exit out of program after serialises data

    Parameters
    ----------
    address_book : dict

    Returns
    -------
    None
    """
    path = Path("data.bin")
    serialize_data(address_book, path)
    sys.exit(f"\n\tThe address book was saved to <{path}> file.\n\tGood bye!")


def serialize_data(some_obj, file_name):
    """Serializes data to given file

    Parameters
    ----------
    some_obj: dict
    file_name: path to the particular file

    Returns
    -------
    None
    """
    with open(file_name, "wb") as f_h:
        pickle.dump(some_obj, f_h)


def input_error(func):
    """Decorator to handle with exeptions

    Parameters
    ----------
    func: func

    Returns
    -------
    wrapper: func
    """

    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except StopIteration:
            ex_info = "\n\tYou have seem all contact's info."
        except (ValueError, KeyError) as ex:
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
        r"\badd\b|\bchange\b|\bphones\b|\bshow\s{1}all\b\
        |\bgood\s{1}bye\b|\bclose\b|\bexit\b|[.]{1}",
        string,
    )
    command = raw_user_input.group() if raw_user_input else False

    # parsing for assigning phone number
    raw_phone = re.search(r"38(097|098|068|067|063|068|099)\d{7}", string)
    phone = raw_phone.group() if raw_phone else False

    # parsing for assigning name
    raw_name = re.search(
        r"(?!.*(add|change|phones|good|bye|close|exit|\.{1})+)\s[a-zA-Z]+\s{1}[a-zA-Z]+",
        string,
    )
    name = raw_name.group().strip().title() if raw_name else False

    data = (name, phone)

    return command, data


def show_all_contacts(address_book):
    """Shows all contacts from phonebook

    Parameters
    ----------
    address_book: dict

    Returns
    -------
    result: as info-string or None
    """
    print(f"\n\tAddress book has <{len(address_book)}> contacts.")
    contacts_num = int(input("\n\tEnter how many rows you preffer to see: "))
    info = address_book.iterator(contacts_num)
    while True:
        print(next(info))
        user_input = input("\n\tDo you want to prosside y|n: ").casefold()
        if user_input == "n":
            result = "\n\tContinue your work with commands."
        return result or None


def show_one_contact_data(address_book):
    """Shows one particular contact from phonebook

    Parameters
    ----------
    address_book: dict

    Returns
    -------
    full info for one contact
    """
    user_input = input(
        "\n\tEnter part of contact full name or phone number: "
    ).casefold()
    return address_book.search_contacts(user_input)


@input_error
def handler_func(command, address_book, data):
    """Calls particular function given as argument

    Parameters
    ----------
    command: str
    address_book: dict
    data: tuple

    Returns
    -------
    result of worked function or ValueError
    """
    if command in COMMANDS:
        if command in ["show all", "good bye", "close", "exit", ".", "phones"]:
            result = COMMANDS[command](address_book)
        else:
            result = COMMANDS[command](address_book, data)
    return result or ValueError


COMMANDS = {
    "add": add_phone,
    "show all": show_all_contacts,
    "good bye": save_and_exit,
    "close": save_and_exit,
    "exit": save_and_exit,
    ".": save_and_exit,
    "change": change_existing_phone,
    "phones": show_one_contact_data,
}


def main():
    """Run full procedure of work with addressbook
    """
    print(
        """
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
    """
    )

    initial_user_comand = input("\n\tWaitting for your comand: ").casefold()

    while not initial_user_comand == "hello":
        print("\n\tIn order to work with address book enter <Hello>")
        initial_user_comand = input("\n\tWaitting for your comand: ").casefold()

    path = Path("data.bin")
    path_exists = path.is_file()

    address_book = deserialize_data(path) if path_exists else AddressBook()

    print("*" * 80)
    print(address_book)
    print("*" * 80)

    if path_exists:
        print(
            f"\n\tYou address book has been restored from <{path}> file,\n\tand it's ready to work."
        )

    else:
        print("\n\tCongratulation, you have created new address book!")

    while True:

        user_command = input("\nWaitting for your comand: ")
        user_command = user_command.casefold()

        command, data = parsing_user_input(user_command)
        print(command, data)

        info = handler_func(command, address_book, data)
        print(info)


if __name__ == "__main__":
    main()
