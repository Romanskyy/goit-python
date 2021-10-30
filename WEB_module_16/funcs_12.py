"""Personal functions and classes module

Include all classes for personal assistant app
"""

from collections import UserDict
from datetime import datetime
import re


class AddressBook(UserDict):

    """The class inherits from UserDict class.

    Creates <dict> for sroting adress book data.

    Methods defined in the class are:

    <add_record(self, name, value)>, takes contact name
    and list of phones as a value parameter,
    returns dict with new info as a key and value in it.

    <iterator(self, n)>, method returns a record generator, takes <n> -
    number of records in <self.data> that will be returned in
    one generator call

    <search_contacts(self, user_input)>, method searches contact's data
    by the given from a user partial info
    """

    def add_record(self, name, value):
        """Adds record with key <name> and value to it

        Parameters
        ----------
        name: str
        value: str

        Returns
        -------
        self.data: dict
        """
        self.data[name] = value
        return self.data

    def iterator(self, num):
        """Function returns <num> records from address_book

        Parameters
        ----------
        num: int

        Returns
        -------
        Info about result func has worked or None
        """
        info = False
        if len(self.data) < num:
            info = "Index is out or range"
        else:
            data_list = list(self.data.items())
            while data_list:
                result = "\n".join(
                    [
                        f'\n\tContact <{el[0]}> has following data:\
                        \n\tbirthday info - {list(el[1].items())[0][1]}\
                        \n\tphon/s - {"; ".join(list(el[1].items())[1][1])}'
                        for el in data_list[:num]
                    ]
                )
                yield result
                data_list = data_list[num:]
        return info or None

    def search_contacts(self, user_input):
        """Function search specified contact from address book

        Parameters
        ----------
        user_input: str, phone number

        Returns
        -------
        Contact data or None
        """
        info_list = []
        for cont in self.data:
            match_name_result = re.search(
                user_input.casefold(), cont.casefold())
            match_phone_result = re.search(
                user_input, " ".join(self.data[cont]["phones"])
            )
            if match_name_result is not None:
                info_list.append({cont: self.data[cont]})
            elif match_phone_result is not None:
                info_list.append({cont: self.data[cont]})
        if len(info_list) == 0:
            result = None
        else:
            cont_info = ""
            for val in info_list:
                for name, info_dict in val.items():
                    cont_info += f'\n\tThe contact {name} has\
        \n\tbirthday info - {list(info_dict.items())[0][1]}\
        \n\tphone/s - {"; ".join(list(info_dict.items())[1][1])}.\n'
            result = cont_info
        return result


class Birthday:
    """The class inherits from Fiel class.

    Creates user's birthday(required attribute).
    """

    def __init__(self, birthday):
        """Constructor Birthday class"""
        self.__birthday = birthday

    @property
    def birthday(self):
        """Function creates class's property with @property decorator"""
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        """Function-setter validates and assign
        value to class's field

        Parameters
        ----------
        birthday: str

        Returns
        -------
        Info-string in case of not correct data or None
        """
        real_time = datetime.now()
        datetime_dirthday = datetime.strptime(birthday, "%d.%m.%Y")
        checking_age = real_time.year - datetime_dirthday.year
        if checking_age >= 100:
            result = "Hey, grandpa! You are too old) Check if \
            you have entered correct birthday date."
        elif real_time.year <= datetime_dirthday.year:
            result = "Hey, baby! You are too young) Check if \
            you have entered correct birthday date."
        self.__birthday = birthday
        return result or None

    def birthday_year(self):
        """Fuction returns the year of birth for contact"""
        return self.__birthday.year


class Name:

    """The class inherits from Fiel class.

    Creates user's name(required attribute) starts from an
    uppercase letter with the following lowercase letters.
    """

    def __init__(self, name):
        """Constructor for Name class"""
        self.__name = None
        self.name = name

    @property
    def name(self):
        """Function creates class's property with @property decorator"""
        return self.__name

    @name.setter
    def name(self, name):
        """Function-setter validates and assign
        value to class's field

        Parameters
        ----------
        name: str

        Returns
        -------
        Info-string in case of not correct data or None
        """
        result = False
        if not len(name.split(" ")) == 2:
            result = "Enter fool name."
        else:
            name = name.casefold().title()
            self.__name = name
        return result or None

    def introdus_instanse(self):
        """Full form or instanse's name"""
        return f"My name is {self.name}"


class Phone:
    """The class inherits from Fiel class.

    Creates user's phone field(optional attribute).
    """

    def __init__(self, phone=None):
        """Constructor for Phone class"""
        if phone is None:
            self.__phone = phone
        else:
            self.__phone = (
                phone.strip()
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
            )

    @property
    def phone(self):
        """Function creates class's property with @property decorator"""
        return self.__phone

    @phone.setter
    def phone(self, phone):
        """Function-setter validates and assign
        value to class's field

        Parameters
        ----------
        phone: str

        Returns
        -------
        None
        """
        phone = (
            phone.strip()
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        self.__phone = phone

    def get_network(self):
        """Simple func to return network's code"""
        return self.phone[:6]


class Record:
    """The class for creating fields for phone book.

    Methods defined in the class:

    <add_contact_phonenumb(self, phone_numb)> - creats new contact's
    phone and appends to other contact's phones stored inside a list
    defined inside constructor while creating class instance,

    <days_to_birthday(self, birthday)> - counts amount of days till
    following birthday if <birthday != None>
    """

    def __init__(self, birthday=None):
        """Constructor for Phone class"""
        self.birthday = birthday
        self.phones = []

    def add_contact_phonenumb(self, phone_numb):
        """Function validates entered phone number
        and adds to contact's list of phones

        Parameters
        ----------
        phone_numb: str

        Returns
        -------
        list of phones
        """
        phone_numb = str(
            phone_numb.strip()
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        self.phones.append(phone_numb)
        return self.phones

    def days_to_birthday(self):
        """Function calculates amount of days till following birthday

        Parameters
        ----------

        Returns
        -------
        amount of days till birthday or info-string
        """
        result = False
        if self.birthday is not None:
            real_time = datetime.now()
            datetime_dirthday = datetime.strptime(self.birthday, "%d.%m.%Y")
            this_year_birthday = datetime_dirthday.replace(year=real_time.year)
            next_year_birthday = datetime_dirthday.replace(
                year=real_time.year + 1)
            this_year_days_count = (this_year_birthday - real_time).days
            next_year_days_count = (next_year_birthday - real_time).days
            result = (
                this_year_days_count
                if real_time.date() < this_year_birthday.date()
                else next_year_days_count
            )
            result = (
                f"\n\tThere are {result} days left until the contact's next birthday"
            )
        return result or "\n\tThere is no birthday date for contact"
