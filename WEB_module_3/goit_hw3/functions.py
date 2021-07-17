import pickle


try:
    from classes import *
except:
    from .classes import *

import nltk
import re
import pymorphy2
import textwrap
import itertools
from datetime import datetime
from pathlib import Path
from prettytable import PrettyTable
from termcolor2 import colored
CONTACTS_FILE = 'contacts.dat'
CONTACTS_DIR = ''
path = CONTACTS_DIR
name_file = CONTACTS_FILE
path_file = Path(path) / name_file

LEN_STR_PRINT = 108+19


def pretty_input(text):
    print(colored(text, color='blue'))
    user_input = input('>>> ')
    print(colored('৹' * LEN_STR_PRINT, color='green'))
    return user_input


def pretty_print(data):
    args_pretty = dict()
    if isinstance(data, str):
        pretty_print_str(data, args_pretty)

    elif isinstance(data, Record):
        record = data
        data = AddressBook()
        data[record.name] = record

        pretty_print_table(data, args_pretty)

    elif isinstance(data, AddressBook):
        pretty_print_table(data, args_pretty)

    elif isinstance(data, Exception):
        pretty_print_exception(data, args_pretty)


def pretty_print_exception(data, args_pretty={}):
    args_pretty.setdefault('color', 'red')
    args_pretty.setdefault('on_color', None)
    args_pretty.setdefault('attrs', ['bold', 'blink'])
    print(colored(data, *args_pretty.values()))


def pretty_print_str(data, args_pretty={}):
    args_pretty.setdefault('color', 'green')
    args_pretty.setdefault('on_color', None)
    args_pretty.setdefault('attrs', [])
    data = [el.ljust(LEN_STR_PRINT) for el in data.split('\n')]
    data = '\n'.join(data)
    print(colored(data, *args_pretty.values()))


def pretty_print_table(data, args_pretty={}, n=10):
    args_pretty.setdefault('color', 'yellow')
    args_pretty.setdefault('on_color', None)
    args_pretty.setdefault('attrs', ['bold'])

    #pretty_print_str(f'всего к выводу {len(data)} записей: ', args_pretty)

    print(colored(data, *args_pretty.values()))


# -----------------серелизация-и-десерелизация----------------------


def deserialize_users(path):
    """using the path "path" reads the file with contacts"""

    with open(path, "rb") as fh:
        addressbook = pickle.load(fh)

    return addressbook


def serialize_users(addressbook, path):
    """saves a file with contacts on the path (object pathlib.Path) to disk"""

    with open(path, "wb") as fh:
        pickle.dump(addressbook, fh)

# -----------------конец-блока-серелизация-и-десерелизация-----------


def error_handler(func):
    # сюда вынесена обработка всех возникающих ошибок в ходе работы программы - как типов и
    # форматов, так и логические (дата рождения в будущем, попытка удалить несуществующий параметр и т.д.)
    def inner(*args):
        # print(type(args[0]), type(args[1]))
        if isinstance(args[-1], AddressBook):
            addressbook = deserialize_users(
                path_file) if Path.exists(path_file) else AddressBook()

        try:
            result = func(*args)
            if isinstance(args[-1], AddressBook):
                serialize_users(addressbook, path_file)
            return result
        except Exception as message:
            # надо здесь изменить на message, чтобы тип возвращаемого был Error (Exception)
            return message
    return inner


@error_handler
def get_handler(res_pars, addressbook):
    # получив результаты работы парсера функция управляет передачей параметров
    # и вызовм соотвествующего обработчика команды

    # -----------функции-работы-с-адресбук------первое-меню------------------------------------------------

    def add_record(addressbook):
        #  сначала создает запись с именем
        #  потом последовательно вызывает функции
        # для заполнения телефона, д/р, заметки, и т.д.
        name = enter_new_correct_name(addressbook)
        if not name:
            return True  # если имя передумали вводить выходим в меню
        record = Record(name)
        addressbook.add_record(record)
        add_phone(record)
        change_bd(record)
        change_adr(record)
        add_eml(record)
        add_note(record)
        return f'в адресную книгу внесена запись: \n{RecordViewKonsole(record).view()}'

    @error_handler
    def change_f(addressbook):

        record = search_record(addressbook)
        pretty_print_table(RecordViewKonsole(record).view())
        pretty_print(menu_change)
        item_number = input('>>>  ')
        return func_change[item_number](record)

    @error_handler
    def delete_f(addressbook):
        name = pretty_input('Введите имя ')
        result = addressbook.del_record(name)
        return result

    def enter_new_correct_name(addressbook):
        name = pretty_input('Введите новое имя ')
        while is_in(addressbook, name) or not name:
            if not name:
                name = pretty_input(
                    'У человека должно быть имя. Введите имя. Передумали ? Enter -выход в предыдущее меню')
            else:
                name = pretty_input(
                    'Введите другое имя. Такое имя уже есть (Enter -выход в предыдущее меню')
            if not name:
                return False
        return name

    def exit_f(*args):
        return 'bye'

    def hello_f(*args):
        return 'Привет! Чем я могу Вам помочь?'

    def help_f(*args):
        return '''формат команд:
        - add - формат: add name phone_number - добавляет новый контакт
        - other phone - формат: other phone name phone_number - добавляет дополнительный телефон в существующую запись
        - show all - формат: show all [N] - показывает всю адресную книгу. N - необязательный параметр - количество одновременно выводимых записей
        - exit/./close/goog bye - формат: exit - остановка работы с программой. Важно! чтобы сохранить все изменения и введенные данные - используйте эту команду
        - phone - формат: phone name - поиск телефона по имени. Можно ввести неполной имя либо его часть - программа выведет все совпадения
        - hello - формат: hello - просто Ваше привествие программе. Доброе слово - оно и для кода приятно)
        - bd add - формат: bd add name dd-mm-YYYY - ввод либо перезапись ранее введенной даты рождения. Соблюдайте формат ввода даты.
        - search - формат: search pattern - поиск совпадений по полям имени и телефонов. Будут выведены все записи в которых есть совпадения'''

    def search(addressbook):
        user_input = pretty_input('Что Вы хотите найти? введите паттерн: ')
        # осуществляет поиск введенной строки во всех текстовых полях адресной книги
        result = addressbook.search(user_input)  # type AddressBook

        if not result:
            raise Exception('По данному запросу ничего не найдено')

        return result

    @error_handler
    def search_bd(addressbook):
        pretty_print(
            'Будем искать всех у кого дни рождения от первой введенной даты до второй введенной даты ')
        data_start = pretty_input('Первая дата (формат дд-мм-гггг) ')
        while True:
            try:

                datetime.strptime(data_start, "%d-%m-%Y")
                break
            except:
                pretty_print_str("Это не дата ")
                data_start = pretty_input(
                    'Еще раз. Первая дата (формат дд-мм-гггг) ')
        data_stop = pretty_input('Вторая дата (формат дд-мм-гггг)')
        try:
            datetime.strptime(data_stop, "%d-%m-%Y")
            result = addressbook.search_birthday(data_start, data_stop)
        except:
            pretty_print("Это не дата . Будем искать в одном дне")
            result = addressbook.search_birthday(data_start)
        return result

    def search_record(adressbook):
        pattern = pretty_input(
            'введите имя записи или часть имени/значения поля, которое однозначно определяет запись: ')
        res = addressbook.search(pattern)

        while len(res) != 1:
            pretty_print_str(f'найдено {len(res)} записей')
            pretty_print_table(AddressBookViewKonsole(res).view())
            pattern = pretty_input(
                'введите более точный запрос или порядковый номер абонента в этой таблице (1/2/...) ')
            try:
                number_choice = int(pattern) - 1
                choice_name = list(res)[number_choice]
                one_record = addressbook[choice_name]
                res = AddressBook()
                res[one_record.name] = one_record

            except:
                res = addressbook.search(pattern)

        name, record = list(res.items())[0]

        pretty_print_str(f'найдена запись с именем {name}')
        return record

    def show_all_f(addressbook, N=10):
        return AddressBookViewKonsole(addressbook).view()

    # -----------закончились-функции-работы-с-адресбук--------первое-меню---------------------------------

    # -----------функции-работы-с-записью------------второе-меню------------------------------------------

    def add_eml(record):
        if isinstance(record, Record):
            email_new = pretty_input(
                'введите e-mail: ')
            if not email_new:
                return 'email не введен'
            record.add_email(email_new)
            return f'в запись добавлен e-mail: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соотвекстует более одной записи'

    def add_note(record):
        if isinstance(record, Record):
            note_new = pretty_input(
                'введите заметку. Дата и время будут добавлены автоматически: ')
            if not note_new:
                return 'заметка  не введена'
            record.add_note(note_new)
            return f'в запись добавлена заметка: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соответствует более одной записи'

    def add_phone(record):
        if isinstance(record, Record):
            # позволяет добавить в запись дополнительный телефон
            phone = pretty_input('Введите номер телефона: ')
            if not phone:
                return 'телефон не введен'
            record.add_phone(phone)
            return f'в запись добавлен новый телефон: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соответствует более одной записи'

    def change_adr(record):
        if isinstance(record, Record):
            # address_old = record.address.__repr__() if record.address else 'пока не задан'
            # pretty_print(f'текущий адрес:  {address_old}')
            address_new = pretty_input('введите адрес ("ввод" - пропустить): ')
            record.add_address(address_new)
            return f'в запись добавлен адрес: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соотвекстует более одной записи'

    def change_bd(record):
        if isinstance(record, Record):
            # birthday_old = record.birthday.__repr__() if record.birthday else 'пока не задан'
            # pretty_print(f'текущий день рождения:  {birthday_old}')
            birthday_str = pretty_input(
                'введите день рождения в формате дд-мм-гггг ("ввод" - пропустить): ')
            if not birthday_str:
                return True
            record.add_birthday(birthday_str)
            return f'в запись добавлен день рождения: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соотвекстует более одной записи'

    def change_eml(record):
        if isinstance(record, Record):
            answer = 'н'
            while answer != 'д':
                number_old_email = pretty_input(
                    'Какой email хотите поменять  ? введите его порядковый номер (1/2/3..) или Enter чтобы вернуться назад ')
                if not number_old_email:
                    return True
                if 0 < int(number_old_email) <= len(record.emails):
                    old_email = record.emails[int(number_old_email)-1].email
                    answer = pretty_input(
                        f'Этот email {EmailViewKonsole(old_email).view()}?(д/н)')
                else:
                    answer = 'н'
                    pretty_print('У абонента нет столько email')
            new_email = pretty_input('Введите новый email ')
            result = record.change_email(old_email, new_email)
            return f'У абонента изменен email: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соответствует более одной записи'

    def change_name(record):

        if isinstance(record, Record):
            name = enter_new_correct_name(addressbook)
            # если имя передумали вводить  то прерываемся, ничего не делаем , выходим в меню
            if not name:
                return True
            addressbook.del_record(record.name)
            record.change_name(name)
            addressbook.add_record(record)
            return f'в записи изменено имя: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соответствует более одной записи'

    def change_phone(record):
        if isinstance(record, Record):
            answer = 'н'
            while answer != 'д':
                number_old_phone = pretty_input(
                    'Какой номер хотите поменять  ? введите его порядковый номер (1/2/3..)  или Enter чтобы вернуться назад ')
                if not number_old_phone:
                    return True
                if 0 < int(number_old_phone) <= len(record.phones):
                    old_phone = record.phones[int(number_old_phone)-1].phone
                    answer = pretty_input(
                        f'Этот номер {PhoneViewKonsole(old_phone).view()}?(д/н)')
                else:
                    answer = 'н'
                    pretty_print('У абонента нет столько номеров')
            new_phone = pretty_input('Введите новый номер ')
            result = record.change_phone(old_phone, new_phone)
            return f'в запись добавлен новый телефон: \n{RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соответствует более одной записи'

    def del_eml(record):
        if isinstance(record, Record):
            answer = 'н'
            while answer != 'д':
                number_old_email = pretty_input(
                    'Какой email хотите удалить  ? введите его порядковый номер (1/2/3..) или Enter чтобы вернуться назад  ')
                if not number_old_email:
                    return True
                if 0 < int(number_old_email) <= len(record.emails):
                    old_email = record.emails[int(number_old_email)-1].email
                    answer = pretty_input(
                        f'Этот номер {EmailViewKonsole(old_email).view()}?(д/н)')
                else:
                    answer = 'н'
                    pretty_print('У абонента нет столько email')
            result = record.del_email(old_email)
            return f'У абонента удален email: \ {RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соответствует более одной записи'

    def del_phone(record):
        if isinstance(record, Record):
            answer = 'н'
            while answer != 'д':
                number_old_phone = pretty_input(
                    'Какой номер хотите удалить  ? введите его порядковый номер (1/2/3..) или Enter чтобы вернуться назад  ')
                if not number_old_phone:
                    return True
                if 0 < int(number_old_phone) <= len(record.phones):
                    old_phone = record.phones[int(number_old_phone)-1].phone
                    answer = pretty_input(
                        f'Этот номер {PhoneViewKonsole(old_phone).view()}?(д/н)')
                else:
                    answer = 'н'
                    pretty_print('У абонента нет столько телефонов')
            result = record.del_email(old_phone)
            return f'У абонента удален номер: \ {RecordViewKonsole(record).view()}'
        return 'такой записи не существует или поисковом шаблону соответствует более одной записи'

    def is_in(addressbook, name):
        return name in addressbook

    # -----------закончились-функции-работы-с-записью------------второе-меню------------------------------------

    def unrecognize_f(res_pars, addressbook):
        print(f'вызвана функция unrecognize. Строка:  {res_pars}')
        COMMANDS = {'add': ['добавить', 'приплюсовать', 'нарастить', 'расширить', 'присовокупить', 'доложить', 'подбросить',
                    'прирастить', 'прибавить', 'приобщить', 'причислить', 'дополнить', 'додать', 'надбавить', 'увеличить', 'привнести',
                            'подбавить', 'присоединить', 'подбавить', 'внести', 'добавляй'],
                    'change': ['изменить', 'модифицировать', 'реконструировать', 'поменять', 'трансформировать', 'преобразовать',
                               'преобразить', 'переделать', 'видоизменить', 'обновить', 'переменить', 'сменить', 'изменить', 'менять', 'заменить'],
                    'remove': ['удалить', 'изьять', 'вытереть', 'выкинуть', 'вытереть', 'стререть', 'очистить', 'убрать', 'исключить',
                               'ликвидировать', 'удаляй', 'вытирай'],
                    'search': ['найти', 'выбрать', 'подобрать', 'показать', 'вывести', 'отобразить', 'искать', 'найди', 'ищи']}

        OBJECTS = {'record': ['имя', 'запись', 'человек', ],
                   'phone': ['телефон', 'номер'],
                   'birthday': ['день', 'дата', 'роды'],
                   'note': ['заметка', 'текст', 'тэг', 'примечание', 'описание', 'напоминание'],
                   'email': ['почта', 'мыло', 'email', 'e-mail', 'emails', 'e-mails', 'электронка'],
                   'adress': ['адрес', 'город', 'улица', 'ул.', 'проспект', 'поселок', 'село', 'деревня', 'бульвар', 'дом', 'квартира',
                              'кв.', 'площадь', 'пос.', 'набережная']}

        def pre_processing_str(raw_str):
            # Эта функция считает, что входящий текст - ОДНО предложение. \
            # осуществляет предварительную обработку строки - \
            # из предложения удаляет стоп-слова, \
            # предложение разбивает на слова и возвращает список слов без стоп-слов

            # получаем список слов
            text_words_list = (nltk.word_tokenize(raw_str))
            # читаем из библиотеки и дополняем список стоп-слов
            stop_words = nltk.corpus.stopwords.words('russian')
            stop_words.extend(['что', 'это', 'так', 'вот', 'быть',
                               'как', 'в', '—', '–', 'к', 'на', '...'])
            # удаляем из списка слов стоп-слова
            prepare_text_words_list = [
                i for i in text_words_list if (i not in stop_words)]
            return prepare_text_words_list

        def find_predictors(sentence, context_list, commands_scoup=COMMANDS, objects_scoup=OBJECTS):
            # получает на вход предварительно обработанный список слов из введенной строки, \
            # словарь возможных значений команд и словарь созможных значений объектов (то, над \
            # чем могут совершаться команды). Возвращает словарь, в котором ключами являются \
            # строки - соотвествующие предикторам, а значениями списки (для объектов которые могут \
            # имень несколько значений - телефоны, e-mail, команды или типы объектов), \
            # и одиночное значение (строка) для имени

            morph_ru = pymorphy2.MorphAnalyzer()

            def find_emails(sentence):
                regex = re.compile('[^ @]*@[^ ]*')
                result = regex.findall(sentence)
                return result if result else None

            def find_selected_text(sentence):
                # выделяет и возвращает из предложения текст, выделенный любой парой
                # (в начале и в конце) знаков ()
                # Если не найдено ничго, возвращает None
                regex = re.compile('[(].+[)]')
                result = regex.search(sentence)
                return result.group()[1:-1] if result else None

            def find_commands(word_of_morph_res, commands_scoup=COMMANDS):
                # из результатов морфлогического разбора отдельных слов выбираю ТОЛЬКО глаголы\
                # и сравниваю их нормальную форму с перечнем возможных команд. При совпадении\
                # возвращаю наименование команды как строку, иначе - None
                if word_of_morph_res.tag.POS == 'VERB' or word_of_morph_res.tag.POS == 'INFN':
                    for key, value in commands_scoup.items():
                        for word in value:
                            if word_of_morph_res.normal_form == word:
                                return key

            def find_objekts(word_of_morph_res, objects_scoup=OBJECTS):
                # из результатов морфлогического разбора отдельных слов выбираю ТОЛЬКО существительные\
                # и сравниваю их нормальную форму с перечнем возможных названий объектов. При совпадении\
                # возвращаю наименование объекта как строку, иначе - None
                res = None
                if word_of_morph_res.tag.POS == 'NOUN':
                    for key, value in objects_scoup.items():
                        res = key if [x for x in value if x ==
                                      word_of_morph_res.normal_form] else None
                        if res:
                            break
                return res

            def find_name(word_of_morph_res):
                # из результатов морфлогического разбора отдельных слов выбираю ТОЛЬКО с признаком,\
                # одушевленности и формирую из них одну строку. Если не найдено ничего - None
                res = []
                for word in word_of_morph_res:
                    # print(f'{word[0].normal_form}    {word[0].tag.animacy}')
                    if word.tag.animacy == 'anim':
                        res.append(word.normal_form)
                return ' '.join(res) if res else None

            def find_phones(sentence):
                regex = re.compile('\+?[0-9-xX()\[\]]{5,25}')
                result = regex.findall(sentence)
                return result if result else None

            predictors_dict = {
                'name': None,
                'selected_text': None,
                'commands': [],
                'objects': [],
                'phones': [],
                'emails': [],
                'context': None
            }
            predictors_dict['selected_text'] = find_selected_text(sentence)
            predictors_dict['phones'] = find_phones(sentence)
            predictors_dict['emails'] = find_emails(sentence)
            prepare_text_words_list = pre_processing_str(sentence)

            # проводим морфологический разбор слов в списке переданных подготовленных слов,\
            #  выбираем только наиболее вероятные знаяения для слов (выбор єлемента с индексом 0)
            morph_ru_result = [morph_ru.parse(word)[0]
                               for word in prepare_text_words_list]

            for word in morph_ru_result:
                command = find_commands(word, commands_scoup=COMMANDS)
                if command:
                    predictors_dict['commands'].append(command)

                object_for = find_objekts(word, objects_scoup=OBJECTS)
                if object_for:
                    predictors_dict['objects'].append(object_for)

            predictors_dict['name'] = find_name(morph_ru_result)

            if predictors_dict['name']:
                predictors_dict['context'] = predictors_dict['name']
            else:
                predictors_dict['context'] = None if len(
                    context_list) == 0 else context_list[-1]
            context_list.append(predictors_dict['context'])

            print(prepare_text_words_list)  # отладочный вывод

            print(predictors_dict)  # отладочный вывод
            if len(predictors_dict['commands']) > 1:
                raise Exception(
                    'Сложные команды разбивайте на предложения: не более одного действия в однм предложении (найти\заменить\добавить...)')
            return predictors_dict

        def handler_raw(predictors_dict, address_book):
            # получает на вход словарь с набором выявленных предикторов \
            # и на основе их анализа предлагает действия для их обработки
            # возвращает строку с рапортом о совершенных действиях или None\
            #  если никакие действия совершены быть не могут

            if ('search' in predictors_dict['commands']) and predictors_dict['selected_text']:
                chois = pretty_input(
                    f'''распознана команда ПОИСК. \n
                            текст в скобках, по всей видимости, является паттерном для поиска:\n
                            паттерн: {predictors_dict['selected_text']}\n
                            Выберите действие:
                                1. поиск по текущему паттерну
                                2. ввести новый паттерн
                                3. поиск по дням рождения (даты и интервалы дат)
                                4. выход
                        ''')
                if chois == '1':
                    return address_book.search(predictors_dict['selected_text'])
                elif chois == '2':
                    return search(address_book)
                elif chois == '3':
                    return search_bd(address_book)
                return True

            elif ('search' in predictors_dict['commands'] and not predictors_dict['selected_text']):
                print('точка 2')
                chois = pretty_input(
                    f'''
                        распознана команда ПОИСК. \n
                        подсказка: текст в круглых скобках в предложении с 
                        командой поиска будет воспринят как паттерн

                        в текущем вводе паттерн не распознан.
                        Выберите действие:
                            1. ввести паттерн для поиска
                            2. поиск по дням рождения (даты и интервалы дат)
                            3. выход
                    ''')
                if chois == '1':
                    return search(address_book)
                elif chois == '2':
                    return search_bd(address_book)
                return True

            if ('add' in predictors_dict['commands']) and (not predictors_dict['name']) and (not predictors_dict['objects']):
                chois = pretty_input(
                    f'''распознана команда ДОБАВИТЬ. \n
                            не распознано имя абонента
                            Выберите действие:
                                1. создать новую запись
                                4. выход
                        ''')
                if chois == '1':
                    return add_record(address_book)
                elif chois == '2':
                    return True
            elif ('add' in predictors_dict['commands']) and predictors_dict['name'] and (not predictors_dict['objects'] or ('record' in predictors_dict['objects'])) and not predictors_dict['phones'] and not predictors_dict['emails']:
                if is_in(address_book, predictors_dict['name']):
                    pretty_print(
                        f"запись с именем {predictors_dict['name']} существует")
                    item_number = pretty_input(menu_change)
                    record = address_book[predictors_dict['name']]
                    pretty_print(record)
                    return func_change[item_number](record)
                pretty_print(
                    f"запись с именем {predictors_dict['name']} не существует. Создаем запись:")
                record = Record(predictors_dict['name'])
                address_book.add_record(record)
                add_phone(record)
                change_bd(record)
                change_adr(record)
                add_eml(record)
                add_note(record)
                return f'в адресную книгу внесена запись: \n{record}'
            elif ('add' in predictors_dict['commands']) and (predictors_dict['name'] or predictors_dict['context']) and predictors_dict['objects'] and (predictors_dict['phones'] or predictors_dict['emails']):
                name = predictors_dict['name'] or predictors_dict['context']
                if is_in(address_book, name):
                    pretty_print(f"""в запись с именем {name} будет добавлены элементы:
                            телефон - {len(predictors_dict['phones'])} шт
                            e-mail  - {len(predictors_dict['emails'])} шт""")
                    choise = pretty_input("""подтвердите операцию:
                            1. продолжить
                            2. отменить""")
                    if choise == '1':
                        record = address_book[name]
                        for phone in predictors_dict['phones']:
                            record.add_phone(phone)
                        for email in predictors_dict['emails']:
                            record.add_email(email)
                        # pretty_table(record)
                        return f"в запись {name} добавлено {len(predictors_dict['phones']) + len(predictors_dict['emails'])} элеметов"
                    return 'операция отменена'
                pretty_print(
                    f'записи с именем {name} - невозможно добавить что-либо. Сначала создайте запись.')
                pretty_print(
                    'При написании команд придерживайтесь правила - одно предложени описывает одно действие.')
                return 'обработка строки завершена'
            elif ('add' in predictors_dict['commands']) and (predictors_dict['name'] or predictors_dict['context']) and predictors_dict['selected_text'] and ('adress' in predictors_dict['objects'] or 'note' in predictors_dict['objects']):
                name = predictors_dict['name'] or predictors_dict['context']
                if is_in(address_book, name):
                    if 'adress' in predictors_dict['objects'] and 'note' in predictors_dict['objects']:
                        pretty_print(
                            f'нельзя за один шаг внести данные и в заметки и в адрес')
                        pretty_print(
                            'разделяйте действия по разным предложениям')
                        return 'обработка строки завершена'
                    elif 'adress' in predictors_dict['objects']:
                        pretty_print(
                            f"в запись {name} будет внесен адрес: \n   {predictors_dict['selected_text']}")
                        chois = pretty_input("""подтвердите действие:
                                1. продолжить
                                2. отменить""")
                        if chois == '1':
                            record = address_book[name]
                            record.add_address(
                                predictors_dict['selected_text'])
                            # pretty_table(record)
                            return f"в запись {name} добавлен адрес"
                        return 'операция отменена'
                    elif 'note' in predictors_dict['objects']:
                        pretty_print(
                            f"в запись {name} будет внесена заметка: \n   {predictors_dict['selected_text']}")
                        chois = pretty_input("""подтвердите действие:
                                1. продолжить
                                2. отменить""")
                        if chois == '1':
                            record = address_book[name]
                            record.add_note(
                                predictors_dict['selected_text'])
                            # pretty_table(record)
                            return f"в запись {name} добавлена заметка"
                        return 'операция отменена'
                pretty_print(
                    f'записи с именем {name} - невозможно добавить что-либо. Сначала создайте запись.')
                pretty_print(
                    'При написании команд придерживайтесь правила - одно предложени описывает одно действие.')
                return 'обработка строки завершена'
            elif ('add' in predictors_dict['commands']) and (predictors_dict['name'] or predictors_dict['context']) and ('birthday' in predictors_dict['objects']):
                name = predictors_dict['name'] or predictors_dict['context']
                if is_in(address_book, name):
                    record = address_book[name]
                    birthday_str = pretty_input(
                        'введите день рождения в формате дд-мм-гггг: ')
                    record.add_birthday(birthday_str)
                    # pretty_table(record)
                    return f'в запись добавлен день рождения: \n {record.birthday.__repr__()}'
                pretty_print(
                    f'записи с именем {name} - невозможно добавить что-либо. Сначала создайте запись.')
                pretty_print(
                    'При написании команд придерживайтесь правила - одно предложени описывает одно действие.')
                return 'обработка строки завершена'

            if ('change' in predictors_dict['commands'] and not (predictors_dict['name'] or predictors_dict['context'])):
                pretty_print(
                    'изменение значений полей невозможно без указания имени записи\n имя записи не распознано')
                return 'обработка строки завершена'
            elif ('change' in predictors_dict['commands']):
                pass

        def gen_record(predictors_dict):
            # получает словарь выделенных из текста параметров и создает объект типа Record с этими параметрами
            record = Record(predictors_dict['name'])
            for elem in predictors_dict['phones']:
                record.add_phone(elem)
            # for elem in predictors_dict['emails']:
            #    record.add_email(elem)
            return record

            # из сырой строки создаем список предложений

        sentences_list = nltk.sent_tokenize(res_pars)
        context_list = []
        for sentence in sentences_list:
            predictors_dict = find_predictors(sentence, context_list)
            pretty_print(handler_raw(predictors_dict, addressbook))

        return 'обработка строки завершена'

    menu_change = '''
    Выберите необходимы пункт меню: 
                            0. Изменить имя
                            1. Добавить номер телефона (в записи может быть несколько разных номеров).
                            2. Изменить номер телефона.
                            3. Удалить номер телефона.
                            4. Добавить e-mail (в записи может быть несколько e-mail).
                            5. Изменить e-mail. 
                            6. Удалить e-mail.
                            7. Добавить/заменить дату рождения (может быть только одна).
                            8. Добавить/заменить почтовый адрес (может быть только один).
                            9. Добавить заметку (заметки не удаляются, они накапливаются).
                '''
    func_change = {'0': change_name,
                   '1': add_phone,
                   '2': change_phone,
                   '3': del_phone,
                   '4': add_eml,
                   '5': change_eml,
                   '6': del_eml,
                   '7': change_bd,
                   '8': change_adr,
                   '9': add_note,
                   }
    HANDLING = {
        '1': add_record,
        '2': change_f,
        '3': delete_f,
        '4': search,
        '5': search_bd,
        '6': show_all_f,
        '7': exit_f,
        'hello': hello_f,
        'exit': exit_f,
        '.': exit_f,
        'good bye': exit_f,
        'close': exit_f,
        'add': add_record,
        'show all': show_all_f,
        'phone': search,
        'search': search,
        'change': change_f,
        'unrecognize': unrecognize_f,
        'help': help_f,
        'other phone': add_phone,
        'bd add': change_bd,
        '': show_all_f
    }

    return HANDLING.get(res_pars)(addressbook) if HANDLING.get(res_pars) else unrecognize_f(res_pars, addressbook)


def parse(input_string):  # --> ('key word', parameter)
    # извлекает команду и параметры из строки, возвращает в виде списка с
    # одним элементом - кортеж из двух элементов: команды и параметры

    def parse_phone(src):
        # функция принимает строку в качестве аргумента и ищет в ней номер телефона (справа)
        # Возвращает кортеж из двух аргументов - все, вплоть до номера телефона (без
        # пробелов слева и справа) и номера телефона. Если номер телефона не найден,
        # вместо него возвращается пустая строка.

        phone_regex = re.compile(r'[+]?[\d\-\(\)]{5,18}\s?$')
        match = phone_regex.search(src)
        if match is None:
            result = (src.strip(), '')
        else:
            result = (src[:match.start()].strip(), match.group())
        return result

    def parse_word(word):
        # фабричная функция. Производит функции синтаксического анализатора для
        # отдельных команд. Возвращает кортеж из команды, строку после команды
        # и номер телефона. Если номер телефона отсутствует, вместо него
        # возвращается пустая строка.

        l = len(word)

        def result(src):
            if src.casefold().startswith(word.casefold()):
                return word, *parse_phone(src[l:].lstrip())

        return result

    parse_scoup = [
        parse_word('hello'),
        parse_word('add'),
        # parse_word('change'),
        parse_word('phone'),
        parse_word('show all'),
        parse_word('exit'),
        parse_word('close'),
        parse_word('good bye'),
        parse_word('.'),
        parse_word('help'),
        parse_word('search'),
        parse_word('other phone'),
        parse_word('bd add')
    ]
    res_pars = [i(input_string) for i in parse_scoup if i(
        input_string)] or [('unrecognize', '', '')]

    return res_pars[0]
