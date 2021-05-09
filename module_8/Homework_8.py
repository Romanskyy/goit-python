from datetime import datetime
from datetime import date
from datetime import timedelta
from collections import defaultdict


def congratulate(birthdays_list):
    """
    The function processes the list of dictionaries with the names of
    people and their dates of birth, sorting into a separate list of
    people whose dates of birth are in the period of the next week and 
    the current weekend.

    For the function to work, you need a Python version of at least 3.9.2.

    The function takes one positional argument, namely a list of
    dictionaries with the names of people and their dates of birth,
    and returns a dictionary with the names of birthday people for
    the current weekend and next work week.
    """

    #  create a defaultdict to collect people's
    #  names with birthday the following week inside default list
    result_birth_dict = defaultdict(list)

    current_date_info = datetime.now().date()
    current_date_info_iso = datetime.now().date().isocalendar()
    weekend_days_numb_iso_list = [6, 7]
    working_days_numb_iso_list = [1, 2, 3, 4, 5]

    for user_info in birthdays_list:

        # user_datetime_birth_info = user_info['birthday']
        user_date_birth_info = user_info['birthday'].date()
        user_date_birth_info_iso = user_info['birthday'].date().isocalendar()

        #  full birthday day name for user date
        full_birthday_weekday_name = user_date_birth_info.replace(
            current_date_info.year).strftime('%A')

        #  change original birthday year to curent one to compare weeks
        user_birth_week_num = user_date_birth_info.replace(
            current_date_info.year).isocalendar().week

        #  curent week number from iso standatrt
        current_week_numb = current_date_info_iso.week

        #  change original birthday weekday info to curent year to compare weekdays
        user_birth_weekday_num = user_date_birth_info.replace(
            current_date_info.year).isocalendar().weekday

        if user_birth_week_num == current_week_numb and user_birth_weekday_num in weekend_days_numb_iso_list:
            result_birth_dict['Monday'].append(user_info['name'])

        elif user_birth_week_num == current_week_numb + 1 and user_birth_weekday_num in working_days_numb_iso_list:
            result_birth_dict[full_birthday_weekday_name].append(
                user_info['name'])

    return result_birth_dict


def printing_clear_info(raw_info_dict):
    """
    The function prints out the contents of the dictionary
    by pre-sorting the dictionary keys, which are days of
    the week from Monday to Friday inclusive
    """

    week_days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    for day in week_days_list:

        for k, v in raw_info_dict.items():
            if day == k and len(v) > 0:
                print(f'{k}: {", ".join(v)}')


def main():

    users = [
        {'name': 'Bob', 'birthday': datetime.strptime(
            '15.05.1989', '%d.%m.%Y')},
        {'name': 'Tom', 'birthday': datetime.strptime(
            '09.05.1975', '%d.%m.%Y')},
        {'name': 'Tim', 'birthday': datetime.strptime(
            '18.05.1990', '%d.%m.%Y')},
        {'name': 'Rob', 'birthday': datetime.strptime(
            '10.05.1993', '%d.%m.%Y')},
        {'name': 'Ave', 'birthday': datetime.strptime(
            '12.05.1965', '%d.%m.%Y')},
        {'name': 'Alice', 'birthday': datetime.strptime(
            '14.05.1997', '%d.%m.%Y')},
        {'name': 'Sara', 'birthday': datetime.strptime(
            '17.05.2000', '%d.%m.%Y')},
        {'name': 'Simona', 'birthday': datetime.strptime(
            '11.05.1990', '%d.%m.%Y')},
        {'name': 'Robert', 'birthday': datetime.strptime(
            '15.05.1981', '%d.%m.%Y')},
        {'name': 'Tomas', 'birthday': datetime.strptime(
            '09.08.1986', '%d.%m.%Y')},
        {'name': 'Max', 'birthday': datetime.strptime(
            '18.05.1975', '%d.%m.%Y')},
        {'name': 'Rima', 'birthday': datetime.strptime(
            '10.03.1978', '%d.%m.%Y')},
        {'name': 'lisa', 'birthday': datetime.strptime(
            '12.02.1982', '%d.%m.%Y')},
        {'name': 'Olivija', 'birthday': datetime.strptime(
            '14.05.1955', '%d.%m.%Y')},
        {'name': 'Serhio', 'birthday': datetime.strptime(
            '17.05.1965', '%d.%m.%Y')},
        {'name': 'Simon', 'birthday': datetime.strptime(
            '11.05.1999', '%d.%m.%Y')}
    ]

    birthday_people_dict = congratulate(users)

    printing_clear_info(birthday_people_dict)


if __name__ == '__main__':
    main()
