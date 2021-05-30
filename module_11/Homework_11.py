from collections import UserDict
from datetime import datetime


class AddressBook(UserDict):

    """
    The class inherits from UserDict class.

    Creates <dict> for sroting adress book data.

    Methods defined in the class are:

    <add_record(self, name, value)>, takes contact name and list of phones as a value parameter,
    returns dict with new info as a key and value in it.

    <iterator(self, n)>, method returns a record generator, takes <n> - number of records in <self.data> that will be returned in 
    one generator call


    """

    def add_record(self, name, value):
        self.data[name] = value
        return self.data

    def iterator(self, n):
        if len(self.data) < n:
            raise Exception(
                f'Amount of records in <Address Book> is less then <n> = {n} you have entered')
        else:
            data_list = list(self.data.items())
            while data_list:
                result = '\n'.join(
                    [f'Contact <{el[0]}> has following contacts {el[1]}' for el in data_list[:n]])
                yield result
                data_list = data_list[n:]


class Field:

    pass


class Birthday(Field):

    """
    The class inherits from Fiel class.

    Creates user's birthday(required attribute).

    """

    def __init__(self, birthday):
        self.__birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        real_time = datetime.now()
        datetime_dirthday = datetime.strptime(birthday, '%d.%m.%Y')
        checking_age = real_time.year - datetime_dirthday.year
        if checking_age >= 100:
            raise Exception(
                f'Hey, grandpa! You are too old) Check if you have entered correct birthday date.')
        elif real_time.year <= datetime_dirthday.year:
            raise Exception(
                f'Hey, baby! You are too young) Check if you have entered correct birthday date.')
        else:
            self.__birthday = birthday


class Name(Field):

    """
    The class inherits from Fiel class.

    Creates user's name(required attribute) starts from an uppercase letter with the following lowercase letters.

    """

    def __init__(self, name):
        self.__name = name.casefold().title()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not len(name.split(' ')) == 2:
            raise Exception('Enter fool name.')
        else:
            name = name.casefold().title()
            self.__name = name


class Phone(Field):

    """
    The class inherits from Fiel class.

    Creates user's phone field(optional attribute).

    """

    def __init__(self, phone=None):
        self.__phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        phone = (
            phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        self.__phone = phone


class Record:

    """
    The class for creating fields for phone book.

    Methods defined in the class:

    <add_contact_phonenumb(self, phone_numb)> - creats new contact's phone and appends to other contact's
    phones stored inside a list defined inside constructor while creating class instance,

    <change_contact_phonenumb(self, phone_numb, new_phone_number)> - changes existing phone number,

    <days_to_birthday(self, birthday)> - counts amount of days till following birthday if <birthday != None>,

    <remove_contact_phonenumb(self, phone_numb)> - removes existing phone number

    """

    def __init__(self, name, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []

    def add_contact_phonenumb(self, phone_numb):
        phone_numb = str(
            phone_numb.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        self.phones.append(phone_numb)
        return self.phones

    def change_contact_phonenumb(self, phone_numb, new_phone_number):
        phone_numb = str(
            phone_numb.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        new_phone_number = str(new_phone_number)
        self.phones.pop(self.phones.index(phone_numb))
        self.phones.append(new_phone_number)
        return self.phones

    def days_to_birthday(self):
        if self.birthday is not None:
            real_time = datetime.now()
            datetime_dirthday = datetime.strptime(self.birthday, '%d.%m.%Y')
            this_year_birthday = datetime_dirthday.replace(year=real_time.year)
            next_year_birthday = datetime_dirthday.replace(
                year=real_time.year + 1)
            this_year_days_count = (this_year_birthday - real_time).days
            next_year_days_count = (next_year_birthday - real_time).days
            result = this_year_days_count if real_time.date(
            ) < this_year_birthday.date() else next_year_days_count
        else:
            result = f'There is no birthday date for contact <{self.name}>'
        return result

    def remove_contact_phonenumb(self, phone_numb):
        phone_numb = str(phone_numb)
        self.phones.pop(self.phones.index(phone_numb))
        return self.phones


def main():
    pass


if __name__ == '__main__':
    main()
