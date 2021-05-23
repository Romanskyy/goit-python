from collections import UserDict


class AddressBook(UserDict):

    """
    The class inherits from UserDict class.

    Creates <dict> for sroting adress book data.

    Method defined in the class is <add_record>, takes contact name and list of phones as a value parameter,
    returns dict with new info as a key and value in it.

    """

    def add_record(self, name, value):
        self.data[name] = value
        return self.data


class Field:

    pass


class Name(Field):

    """
    The class inherits from Fiel class.

    Creates user's name(required attribute) starts from an uppercase letter with the following lowercase letters.

    """

    def __init__(self, name):
        self.name = name.casefold().title()


class Phone(Field):

    """
    The class inherits from Fiel class.

    Creates user's phone field(optional attribute).

    """

    phone = None


class Record:

    """
    The class for creating fields for phone book.

    Methods defined in the class:

    <add_contact_phonenumb(self, phone_numb)> - creats new contact's phone and appends to other contact's
    phones stored inside a list defined inside constructor while creating class instance,

    <change_contact_phonenumb(self, phone_numb, new_phone_number)> - changes existing phone number,

    <remove_contact_phonenumb(self, phone_numb)> - removes existing phone number

    """

    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_contact_phonenumb(self, phone_numb):
        phone_numb = str(phone_numb)
        self.phones.append(phone_numb)
        return self.phones

    def change_contact_phonenumb(self, phone_numb, new_phone_number):
        phone_numb = str(phone_numb)
        new_phone_number = str(new_phone_number)
        self.phones.pop(self.phones.index(phone_numb))
        self.phones.append(new_phone_number)
        return self.phones

    def remove_contact_phonenumb(self, phone_numb):
        phone_numb = str(phone_numb)
        self.phones.pop(self.phones.index(phone_numb))
        return self.phones


def main():
    pass


if __name__ == '__main__':
    main()
