"""Personal assistant test module

The script makes tests for personal assistant's
classes, functions and methods
"""

import pytest
from main_12 import (
    inner_parser,
    add_phone,
    deserialize_data,
    parsing_user_input,
    handler_func,
    show_one_contact_data,
    serialize_data,
    change_existing_phone,
    save_and_exit,
    show_all_contacts,
    main)
from funcs_12 import Name, Phone, Record, AddressBook, Birthday


def test_inner_parser():
    """Inner_parser test func"""
    data = ('Romanskyy Andrey', '380675119811')
    assert inner_parser(data) == (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)


def test_add_phone():
    """Test-func for <add_phone> function"""
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
    """Fixture for <test_deserialize_data> function"""
    some_dict = {"test": 1}
    return some_dict


def test_deserialize_data(empty_dict: dict):
    """Test-func for <deserialize_data> function"""
    path = 'test_data.bin'
    serialize_data(empty_dict, path)
    assert deserialize_data(path) == empty_dict


@pytest.fixture
def wrong_dict():
    """Fixture for <deserialize_data> function with wrong data"""
    wrong_dict = {"wrong_test": 2}
    return wrong_dict


def test_wrong_deserialize_data(empty_dict: dict, wrong_dict: dict):
    """Test-func for <deserialize_data> function with wrong data"""
    path = 'test_wrong_data.bin'
    serialize_data(empty_dict, path)
    assert deserialize_data(path) != wrong_dict


def test_parsing_user_input():
    """Test-func for <parsing_user_input> function"""
    correct_input = 'add Andrey Romanskyy 380675119811'
    bad_phone = 'add Andrey Romanskyy 876876876876876'
    bad_name = 'add AndreyRomanskyy 380675119811'
    incorrect_input = 'some lsoij lkjlkj'

    assert parsing_user_input(correct_input) == (
        'add', ('Andrey Romanskyy', '380675119811'))
    assert parsing_user_input(bad_phone) == (
        'add', ('Andrey Romanskyy', False))
    assert parsing_user_input(bad_name) == (
        'add', (False, '380675119811'))
    assert parsing_user_input(incorrect_input) == (
        (False, ('Lsoij Lkjlkj', False))
    )


def test_search_contacts():
    """Test-func for <search_contacts> function"""
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
    assert address_book.search_contacts(wrong_data) is None


def test_handler_func():
    """Test-func for <handler_func> function"""
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

    assert handler_func(show_command, address_book, data) == (
        '\n\tContinue your work with commands.'
    )
    assert handler_func(show_command, address_book, data) == show_result
    assert handler_func(show_command, address_book, data) == show_result
    assert handler_func(add_command, address_book, data) == add_result


def test_show_one_contact_data():
    """Test-func for <show_one_contact_data> function"""
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
    """Test-func for <serislize_data> function"""
    example_data = {'some': 10}
    path = 'some.bin'

    assert serialize_data(example_data, path) is None


def test_get_network():
    """Test-func for <get_network> method"""
    raw_num = '3(8067)511-98-11'
    result = '067'
    assert Phone(raw_num).get_network() == result


def test_add_contact_phonenumber():
    """Test-func for <add_contact_phonenumber> method"""
    record = Record()
    record.add_contact_phonenumb('3(8067)511-98-11')
    result = ['380675119811']
    assert record.phones == result


def test_days_to_birthday():
    """Test-func for <days_to_birthday> method"""
    rom = Record('03.06.1978')
    assert rom.days_to_birthday() == (
        "\n\tThere are 214 days left until the contact's next birthday"
    )


def test_add_record():
    """Test-func for <add_record> method"""
    assert AddressBook().add_record(
        'Andrey Romanskyy', '380575119811'
    ) == {'Andrey Romanskyy': '380575119811'}

    assert AddressBook().add_record(
        'Andrey Romanskyy', '380575119811'
    ) != 'Andrey Romanskyy=380575119811'


def test_birthday():
    """Test-func for <birthday> field"""
    assert Birthday('03.06.1978').birthday == '03.06.1978'


def test_name():
    """Test-func for <name> field"""
    assert Name('Romanskyy Andrey').name == 'Romanskyy Andrey'


def test_introduse_instanse():
    """Test-func for <introduse_instanse> method"""
    assert Name('Romanskyy Andrey').introduse_instanse() == (
        'My name is Romanskyy Andrey'
    )


def test_record():
    """Test-func for <Record> class"""
    rec = Record('03.06.1978')
    rec.add_contact_phonenumb('38(0676665544)')
    rec.add_contact_phonenumb('38(0676)665--544)')
    assert rec.birthday == '03.06.1978'
    assert rec.phones == ['380676665544', '380676665544']


def test_change_existing_phone():
    """Test-func for <change_existing_phone> method"""
    address_book = AddressBook()
    name, phone = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record = Record()
    record.add_contact_phonenumb(phone)
    address_book.add_record(name, record.__dict__)

    data = ('Romanskyy Andrey', '380675119811')
    assert change_existing_phone(address_book, data) == (
        "\n\t<380675119811> for contact <Romanskyy Andrey>\n\twas changed for <380675119812>."
    )


def test_change_error():
    """Test-func for <change_existing_phone> method"""
    address_book = AddressBook()
    name, phone = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record = Record()
    record.add_contact_phonenumb(phone)
    address_book.add_record(name, record.__dict__)

    data = ('Romanskyy Andrey', '380675119811')

    assert change_existing_phone(address_book, data) == (
        '\n\tEnter correct number.'
    )


def test_exit():
    """Test-func for <exit> func"""
    address_book = AddressBook()
    name, phone = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record = Record()
    record.add_contact_phonenumb(phone)
    address_book.add_record(name, record.__dict__)

    with pytest.raises(SystemExit) as pytest_exit:
        save_and_exit(address_book)
    assert pytest_exit.type == SystemExit
    assert pytest_exit.value.code == (
        "\n\tThe address book was saved to <data.bin> file.\n\tGood bye!"
    )


def test_show_all_contacts():
    """Test-func for <show_all_contacts> func"""
    address_book = AddressBook()

    name_one, phone_one = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record_one = Record()
    record_one.add_contact_phonenumb(phone_one)
    address_book.add_record(name_one, record_one.__dict__)

    name_two, phone_two = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record_two = Record()
    record_two.add_contact_phonenumb(phone_two)
    address_book.add_record(name_two, record_two.__dict__)

    # use <n>
    assert show_all_contacts(address_book) == (
        '\n\tContinue your work with commands.'
    )

    # use <y>
    with pytest.raises(StopIteration) as pytest_si:
        show_all_contacts(address_book)
    assert pytest_si.type == StopIteration
    # assert pytest_exit.value.code == (
    #     "\n\tThe address book was saved to <data.bin> file.\n\tGood bye!"
    # )


def test_main():
    """Test-func for <main> func"""
    address_book = AddressBook()

    name_one, phone_one = (
        Name('Romanskyy Andrey').name, Phone('380675119811').phone)
    record_one = Record()
    record_one.add_contact_phonenumb(phone_one)
    address_book.add_record(name_one, record_one.__dict__)

    with pytest.raises(SystemExit) as pytest_main:
        main()
    assert pytest_main.type == SystemExit
    assert pytest_main.value.code == (
        "\n\tThe address book was saved to <data.bin> file.\n\tGood bye!"
    )
