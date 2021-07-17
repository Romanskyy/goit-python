
from collections import UserDict
from datetime import datetime, date, timedelta
from faker import Faker
import re
from prettytable import PrettyTable
from termcolor2 import colored
import textwrap
import itertools
from abc import abstractmethod, abstractproperty, ABC

LEN_STR_PRINT = 108+19


class Note(UserDict):
    """
    FOR JUST IN CASE
    def __init__(self, data=None):
        super(Note, self).__init__()
        self[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = data
    """

    def add_note(self, data):
        self[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = data

    def __repr__(self):
        result = ''
        log = f'Заметка не создана.'
        for k, v in self.items():
            result += f'{k} - {v}\n'
        result = result if result else log
        return result


class Email:
    def __init__(self, email):
        self.__email = None
        self.email = email

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.email == other.email
        if isinstance(other, str):
            return self.email == other

    @ property
    def email(self):
        return self.__email

    @ email.setter
    def email(self, email):
        regex = r'\b[a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]*\.[a-zA-Z]{2,}\b'
        log = 'email имеет ошибочный формат'
        raw_email = re.search(regex, email)
        if raw_email != None:
            email = raw_email.group()
            self.__email = email
        else:
            raise ValueError(log)

    def __repr__(self):
        return self.email


class Phone:
    # класс для хранения и предварительно обработки номера телефона

    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    def __eq__(self, ob) -> bool:
        # два объекта равны если равны строковые значения сохраненных телефонов
        if isinstance(ob, Phone):
            return self.phone == ob.phone
        if isinstance(ob, str):
            return self.phone == ob

    @ property
    def phone(self):
        return self.__phone

    @ phone.setter
    def phone(self, phone):
        num = phone.translate(str.maketrans('', '', '+() -_'))
        if num.isdigit() and (5 <= len(num) <= 20):
            self.__phone = num
        else:
            raise ValueError(
                'Телефон при вводе может содержать от 5 до 20 цифр и символы: пробел +-()xX.[]_')

    def __repr__(self):
        x = self.phone
        s = f'+{x[:2]}({x[2:4]})-{x[4:7]}-{x[7:]}'

        return s


class Birthday:
    # класс для храниения и предварительной обработки даты рождения. Данные вводятся в строковом
    # виде и отображаются в строковом виде, хранятся в виде объекта datetime
    def __init__(self, date_str):
        self.__birthday = None
        self.birthday = datetime.strptime(date_str, "%d-%m-%Y")

    @ property
    def birthday(self):
        return self.__birthday

    @ birthday.setter
    def birthday(self, new_value):
        if isinstance(new_value.date(), date):
            if new_value.date() > date.today():
                raise ValueError('введенная дата роджения в будущем')
            self.__birthday = new_value
        else:
            raise TypeError('поле Birthday.birthday должно быть типа datetime')

    def __repr__(self):
        return self.birthday.strftime('%d-%m-%Y')


class Record:
    # класс для хранения данных об одном человеке. Тк же содержит методы обработки этой записи
    def __init__(self, name, birthday=None, address=None):
        # обязательное поле name
        self.name = name
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None
        self.emails = []  # DONE
        self.note = Note()
        self.address = address

    def add_address(self, address):
        if isinstance(address, str):
            self.address = address
            return self.address
        else:
            raise TypeError('Адрес должен иметь строковый формат данных.')

    def change_name(self, name):
        self.name = name
        return self

    def add_phone(self, phone):
        # добавляет номер телефона в существующую запись. Если такой номер есть - генерирует исключение
        if Phone(phone) in self.phones:
            raise ValueError(
                'добавление телефона: такой номер уже есть в списке')
        else:
            self.phones.append(Phone(phone))
        return self

    def add_email(self, email):
        email = Email(email)
        if email not in self.emails and email != 'email имеет ошибочный формат':
            self.emails.append(email)
        else:
            raise ValueError(
                'Введенный адрес электронной почты уже есть в контактных данных.')

    def del_email(self, email):
        email = Email(email)
        if email in self.emails:
            self.emails.remove(email)
        else:
            raise ValueError(
                'Невозможно удалить несуществующий адрес электронной почты.')

    def change_email(self, old_email, new_email):
        self.del_email(self, old_email)
        self.add_email(self, new_email)

    def add_note(self, note):
        self.note[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = note

    def del_phone(self, phone):
        # удаляет телефон из записи. При попытке удалить несуществующий номер
        # телефона - генерирует исключение
        if Phone(phone) in self.phones:
            self.phones.remove(Phone(phone))
        else:
            raise ValueError(
                'операция удаления: такого телефона нет в данной записи')

    def change_phone(self, old_phone, new_phone):
        # замена номера телефона - удаление старого и добавление нового
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def days_tobirthday(self):
        if self.birthday:
            if date.today() > self.birthday.replace(year=date.today().year):
                return (self.birthday.replace(year=date.today().year + 1) - date.today()).days
            return (self.birthday.replace(year=date.today().year) - date.today()).days
        return f'Не введена дата родения для {self.name.value}'

    def __repr__(self):
        # форматирует и выводит одну запись в читаемом виде одной или нескольких строк
        # (если запись содержит несколько телефонов)
        output_str = '_' * 80 + '\n' + \
            f"|{'имя':^25}|{'дата':^10}|{'телефоны':^16}|{'e-mails':^24}|\n" + \
            '_' * 80 + '\n'

        str_num = max(len(self.name.split()), len(
            self.phones), len(self.emails))
        name_list = []
        phones_list = []
        emails_list = []
        birthday_list = []
        for i in range(str_num):
            if i == 0:
                birthday_list.append(self.birthday.__repr__())
            else:
                birthday_list.append('')
            if len(self.name.split()) > i:
                name_list.append(self.name.split()[i])
            else:
                name_list.append('')

            if len(self.phones) > i:
                phones_list.append(self.phones[i].__repr__())
            else:
                phones_list.append('')

            if len(self.emails) > i:
                emails_list.append(self.emails[i])
            else:
                emails_list.append('')
            output_str += f"|{name_list[i]:^25}|{birthday_list[i]:^10}|{phones_list[i]:>16}|{emails_list[i]!r:>24}|\n"
        output_str += '_' * 80 + '\n'
        output_str += f"| {'Адрес:':<7}|\n"
        count = 0
        if self.address:
            for i in range(round(len(self.address) / 74 + 0.5)):
                output_str += f"|    {self.address[count:count + 74]:<74}|\n"
                count += 74
        else:
            output_str += f"|    {'поле не заполнено':^78}|\n"
        output_str += '_' * 80 + '\n'
        output_str += f"| {'Заметки:':<77}|\n"
        for key, value in self.note.items():
            count = 0
            elem = key + ' ' + value
            for i in range(round(len(elem) / 74 + 0.5)):
                output_str += f"|    {elem[count:count + 74].__repr__():<74}|\n"
                count += 74
        output_str += '_' * 80 + '\n'
        return output_str

    def add_birthday(self, birthday):
        # добавляет день рождения в существующую запись
        self.birthday = Birthday(birthday)

    def search_birthday(self, data_start, data_stop=False, year: bool = False):
        # если дата рождения находится в интервале от data до data_stop\
        # возвращает экзкмпляр записи, иначе возвращает False. Если \
        # date_stop=False, то сравнение проходит не по интервалу дат, а по\
        # одной дате date. Если year=False - то при сравнении год не \
        # учитывается, иначе год участвует в сравнении
        if not self.birthday:
            # если дата рождения не записана - возвращаем None
            return None

        data_start_local = datetime.strptime(data_start, "%d-%m-%Y")
        data_stop_local = datetime.strptime(
            data_stop, "%d-%m-%Y") if data_stop else datetime.strptime(data_start, "%d-%m-%Y") + timedelta(days=1)
        data_record_local = self.birthday.birthday

        if not year:
            # если year=False то все даты приводятся к текущему году (сравниваются только\
            # по числу и месяцу )
            current_year = date.today().year
            data_start_local = data_start_local.replace(year=current_year)
            data_stop_local = data_stop_local.replace(year=current_year)
            data_record_local = data_record_local.replace(year=current_year)

        if data_start_local <= data_record_local < data_stop_local:
            return self
        # если дата рождения попадает в интервал - возвращаем экземпляр записи, иначе False
        return False

    def search(self, pattern):
        # просматривает текстовые поля записи (name, phones, note, address, emails). Если встречает \
        # сответствие паттерну - возвращает экземпляр записи. Иначе возвращает\
        # False
        if pattern.casefold() in self.name.casefold():
            return self
        if self.address:
            if pattern.casefold() in self.address.casefold():
                return self
        if self.note:
            for value in self.note.values():
                if pattern.casefold() in value:
                    return self
        if self.phones:
            for phone in self.phones:
                if pattern.casefold() in phone.phone.casefold():
                    return self
        if self.emails:
            for email in self.emails:
                if pattern.casefold() in email.email.casefold():
                    return self

        return False


class AddressBook(UserDict):

    def out_iterator(self, n):
        '''
        метод возвращает на каждой итерации объект класса AddressBook,
        содержащий n записей из вызывающего метод объекта AddressBook,
        на последнем шаге (исчерпание записей вызывающего объекта) выводятся
        оставшиеся записи
        '''
        # количество элементов выводимых за один вызов метода
        self.n = n
        # счетчик общего количества выведенных записей
        self.k = 0
        # список из ключей вызывающего метод объекта AddressBook
        key_list = list(self)
        # общее кличество записей, которые должны быть выведены
        key_list_max = len(key_list)
        while self.k < key_list_max:
            result = AddressBook()
            # определяем сколько записей можно вывести на текущем шаге (пна последнем шаге
            # выводим меньше чем n)
            max_iter = key_list_max if len(
                key_list[self.k:]) < self.n else self.k + self.n
            for i in range(self.k, max_iter):
                result.add_record(self[key_list[i]])
                self.k += 1
            yield result

    def add_record(self, record: Record):
        # добавляет новую запись в существующую адрессную книгу.
        # Если запись с таким ключем (именем) уже существует - генерирует исключение
        if record.name in self:
            raise KeyError(
                'Запись с таким именем уже существует в адресной книге')
        self[record.name] = record

    def del_record(self, name: str):
        # удаляет запись с ключем name (строка)
        # из существующей адресной книги. Если такого имени нет - генерирует исключение
        if name in self:
            return self.pop(name)
        else:
            raise KeyError('записи с таким именем нет в адресной книге')

    def search(self, pattern):
        # возвращает объект класса AdressBook, содержащий
        # все записи, которые при проверке методом Record.search вернут значение
        result = AddressBook()
        for record in self.values():
            res_rec = record.search(pattern)
            if res_rec:
                result.add_record(res_rec)
        return result

    def search_birthday(self, data_start, data_stop=False, year: bool = False):
        # возвращает объект класса AdressBook, содержащий записи, для которых \
        # день рождения попадает в интервал дат data_start и data_stop. \
        # Для всех аргументов действуют те же правила, что и для метода \
        # Birthday.search_bithday()
        result = AddressBook()
        for record in self.values():
            res_rec = record.search_birthday(data_start, data_stop, year)
            if res_rec:
                result.add_record(res_rec)
        return result

    def __repr__(self) -> str:
        res = ''
        for elem in self.values():
            res += elem.__repr__()
        return res

    def add_fake_records(self, n):
        fake = Faker(['uk_UA', 'ru_RU'])
        for i in range(n):
            name = fake.name()
            phone = fake.phone_number()
            date_of_birth = fake.date_of_birth(
                minimum_age=10, maximum_age=115).strftime('%d-%m-%Y')
            record = Record(name, date_of_birth).add_phone(phone)
            self.add_record(record)
            # что это здесь делает ?
            print(f'Добавлена запись: {name}  {date_of_birth}  {phone}')


class Window:
    w = {'тип выводимых данных':  "представление"}


class Viewable(ABC):
    @abstractmethod
    def view(self):
        pass


class NoteViewKonsole(Viewable):
    def __init__(self, data: Note):
        self.__dict__ = data.__dict__

    def view(self):
        result = ''
        for k, v in self.data.items():
            result += f'{k} - {v}\n'
        return result


class EmailViewKonsole(Viewable):
    def __init__(self, data: Email):
        self.email = data.email

    def view(self):
        return self.email


class PhoneViewKonsole(Viewable):
    def __init__(self, data: Phone):
        self.phone = data.phone

    def view(self):
        x = self.phone
        s = f'+{x[:2]}({x[2:4]})-{x[4:7]}-{x[7:]}'

        return s


class BirthdayViewKonsole(Viewable):
    def __init__(self, data: Birthday):
        self.birthday = data.birthday

    def view(self):
        return self.birthday.strftime('%d-%m-%Y')


class RecordViewKonsole(Viewable):
    def __init__(self, data: Record):

        self.__dict__ = data.__dict__

    def create_table(self):
        '''
            Данная функция создает таблицу для одной записи в нужном нам виде,
            1. Принимает запись
            2. Парсит ее
            3. Добавляет обработанную инфу в таблицу
            4. Возвращает таблицу как str
            '''
        # from prettytable import ORGMODE
        # ஃ ৹ ∘"܀" "܅" ྿ ፠ ᎒ ። ᠃

        # -----  вид таблицы. заголовок, размеры колонок , разделитители
        table = PrettyTable([], vertical_char="ஃ",
                            horizontal_char="৹", junction_char="ஃ")
        titles = ('имя'.center(20), 'дата рождения'.center(15), 'телефоны'.center(
            18), 'email'.center(20), 'адрес'.center(20), 'заметки'.center(15))
        table.field_names = titles
        table.align = 'l'
        # table.align['заметки'.center(15)] = 'l'

        '''каждый абонент в каждом поле может иметь несколько строк
            поэтому каждое поле разбивается на список строк
            Получим, что у каждого абонента поля это списки строк разной длины
            После этого zip_longest  их соединяет по наибольшей длине
            И полученный результат - список списков поэлементно добавляем в таблицу'''
        name = self.name.split()  # имя  превращаем в список
        # день рождения один, поэтому делаем список из одного элемента
        bd = ['' if not self.birthday else BirthdayViewKonsole(
            self.birthday).view()]

        # телефоны - в список их строчных представлений
        phone = [PhoneViewKonsole(phone).view() for phone in self.phones]

        # emails - попытка разбить на строки
        # можно и нужно сделать лучше
        # по 20 символов без разрывов
        w_em = textwrap.TextWrapper(width=20, break_long_words=True)
        email = w_em.wrap(
            ' \n'.join([EmailViewKonsole(email).view() for email in self.emails]))

        # адрес хорошо разбился на строки
        # по 20 символов без разрывов слов
        w_ad = textwrap.TextWrapper(width=20, break_long_words=True)
        address = w_ad.wrap(self.address or '')

        # заметки тоже должны разбиваться
        # без разрывов слов
        w_no = textwrap.TextWrapper(width=15, break_long_words=True)
        note = NoteViewKonsole(self.note).view()
        note = w_no.wrap(note or '')

        # склеиваем зипом
        x = list(itertools.zip_longest(
            name, bd, phone, email, address, note, fillvalue=""))

        # все элементы списка списков
        # добавляем  в таблицу
        for lst in x:
            table.add_row(lst)

        return table.get_string()

    def view(self):

        # форматирует и выводит одну запись в читаемом виде одной или нескольких строк
        return self.create_table()


class AddressBookViewKonsole(Viewable):
    def __init__(self, data: AddressBook):
        self.__dict__ = data.__dict__

    def view(self):
        res = ''

        for i, elem in enumerate(self.data.values()):

            block = RecordViewKonsole(elem).view()
            if i:
                block = block.split('\n')
                block = '\n'.join(block[3:])

            res += '\n' + block

        return res


if __name__ == '__main__':
    pass
