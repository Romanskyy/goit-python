import pytest
from main_12 import (
    inner_parser,
    add_phone,
    serialize_data,
    deserialize_data,
    parsing_user_input,
    handler_func,
    show_one_contact_data,
    save_and_exit,
    serialize_data,)
from funcs_12 import Name, Phone, Record, AddressBook


def test_inner_parser():
    data = ('Romanskyy Andrey', '380675119811')
    assert inner_parser(data) == (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)


def test_add_phone():
    address_book = AddressBook()
    name, phone = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record = Record()
    record.add_contact_phonenumb(phone)
    address_book.add_record(name, record.__dict__)

    datacase_one = ('Zivenko Kos', '380675119812')
    result_one = (
        "\n\tThe contact <Zivenko Kos> was added to address book with phone <380675119812>."
    )

    datacase_two = ('Romanskyy Andrey', '380675119811')
    result_two = (
        "\n\tThe contact's data is already in address book."
    )

    datacase_three = ('Romanskyy Andrey', '380675119822')
    result_three = (
        "\n\tThe phone <380675119822> for contact <Romanskyy Andrey>\n\t\
        was successfully added to address book."
    )

    assert add_phone(address_book, datacase_one) == result_one
    assert add_phone(address_book, datacase_two) == result_two
    assert add_phone(address_book, datacase_three) == result_three


@pytest.fixture
def empty_dict():
    some_dict = {"test": 1}
    return some_dict


def test_deserialize_data(empty_dict: dict):
    path = 'test_data.bin'
    serialize_data(empty_dict, path)
    assert deserialize_data(path) == empty_dict


@pytest.fixture
def wrong_dict():
    wrong_dict = {"wrong_test": 2}
    return wrong_dict


def test_wrong_deserialize_data(empty_dict: dict, wrong_dict: dict):
    path = 'test_wrong_data.bin'
    serialize_data(empty_dict, path)
    assert deserialize_data(path) != wrong_dict


def test_parsing_user_input():
    correct_input = 'add Andrey Romanskyy 380675119811'
    bad_phone = 'add Andrey Romanskyy 876876876876876'
    bad_name = 'add AndreyRomanskyy 380675119811'

    assert parsing_user_input(correct_input) == (
        'add', ('Andrey Romanskyy', '380675119811'))
    assert parsing_user_input(bad_phone) == (
        'add', ('Andrey Romanskyy', False))
    assert parsing_user_input(bad_name) == (
        'add', (False, '380675119811'))


def test_search_contacts():
    address_book = AddressBook()
    name, phone = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record = Record()
    record.add_contact_phonenumb(phone)
    address_book.add_record(name, record.__dict__)

    contact_data = 'romans'
    wrong_data = 'some'

    result = '\n\tThe contact Romanskyy Andrey has\
        \n\tbirthday info - None\
        \n\tphone/s - 380675119811.\n'

    assert address_book.search_contacts(contact_data) == result
    assert address_book.search_contacts(wrong_data) != result


def test_handler_func():
    address_book = AddressBook()
    name, phone = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record = Record()
    record.add_contact_phonenumb(phone)
    address_book.add_record(name, record.__dict__)

    show_command = 'show all'
    show_result = "\n\tYou have seen all contact's info."

    data = ('Nata Bazan', '380675554433')
    add_command = 'add'
    add_result = '\n\tThe contact <Nata Bazan> was added to address book with phone <380675554433>.'

    assert handler_func(show_command, address_book, data) == show_result
    assert handler_func(add_command, address_book, data) == add_result


def test_show_one_contact_data():
    address_book = AddressBook()
    name, phone = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record = Record()
    record.add_contact_phonenumb(phone)
    address_book.add_record(name, record.__dict__)

    result = '\n\tThe contact Romanskyy Andrey has\
        \n\tbirthday info - None\
        \n\tphone/s - 380675119811.\n'

    wrong_result = None

    assert show_one_contact_data(address_book) == result
    assert show_one_contact_data(address_book) == wrong_result


def test_serislize_data():
    example_data = {'some': 10}
    path = 'some.bin'

    assert serialize_data(example_data, path) is None


def test_get_network():
    raw_num = '3(8067)511-98-11'
    result = '067'
    assert Phone(raw_num).get_network() == result


def test_add_contact_phonenumber():
    record = Record()
    record.add_contact_phonenumb('3(8067)511-98-11')
    result = ['380675119811']
    assert record.phones == result


def test_days_to_birthday():
    rom = Record('03.06.1978')
    assert rom.days_to_birthday() == (
        "\n\tThere are 215 days left until the contact's next birthday"
    )
