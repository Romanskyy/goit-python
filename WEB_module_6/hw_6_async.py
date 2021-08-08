import sys
from pathlib import Path
import shutil
import os
import aiopathlib
import aioshutil
import aiopath
import asyncio


def dir_creator(dirs_list, path_to_create):
    """
    The function creates new directories in shown directory.

    Takes two arguments, namely the list of dirs names and directory path for new dirs creation.
    """

    #  check if given list is not empty
    dirs_exists = len(dirs_list) > 0

    #  creates Path obj
    path = Path(path_to_create)

    new_pathes_list = []

    if dirs_exists and path.is_dir():
        for fold_name in dirs_list:
            new_folder = path.joinpath(fold_name)

            #  check if created new path to future
            #  folder not exists and creats one if not
            if not new_folder.exists():
                new_pathes_list.append(str(new_folder))
                new_folder.mkdir()
            else:
                new_pathes_list.append(str(new_folder))
        result = tuple(new_pathes_list)
        sep = '=' * 75
        print(f'{sep}\nDirs {result} were created successfully.\n')
        return result
    else:
        print(
            f'Something went wrong while dir_creator func worked')


async def folder_processing(path, *new_dirs):
    """
    The function goes to the maximum nesting depth of the specified
    folder and sorts the files into new folders by type .

    Takes two arguments, namely the directory path,
    as an argument when called from the command line,
    and *new_dirs takes an indefinite number of arguments.

    path: full path to the folder for working with one.
    *new_dirs: a collection of an indefinite number of arguments.
    """

    images, documents, audio, video = new_dirs

    if await path.is_dir() and path.stem not in ('archives', 'video', 'audio', 'documents', 'images'):

        async for element in path.iterdir():

            await folder_processing(element, *new_dirs)

            is_folder = await element.is_dir()
            if is_folder:
                dir_name = element.name
                parent_to_dir_path = element.parent
                if path.name.startswith('.'):
                    continue
                else:
                    normalized_dir_name = parent_to_dir_path.joinpath(
                        normalize(dir_name))
                    os.rename(element, normalized_dir_name)

    else:
        current_file_name = path
        parent_to_file_path = path.parent
        name_to_normalize = path.stem
        if path.name.startswith('.'):
            pass
        else:

            normalized_file_name = str(parent_to_file_path.joinpath(
                normalize(name_to_normalize))) + path.suffix
            os.rename(current_file_name, normalized_file_name)
            path = aiopath.AsyncPath(normalized_file_name)

            if path.suffix.upper() in ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']:
                src = path
                documents = aiopath.AsyncPath(documents)
                dst = documents.joinpath(path.name)
                await aioshutil.move(src, dst)
            elif path.suffix.upper() in ['.JPEG', '.PNG', '.JPG', '.SVG']:
                src = path
                images = aiopath.AsyncPath(images)
                dst = images.joinpath(path.name)
                await aioshutil.move(src, dst)
            elif path.suffix.upper() in ['.AVI', '.MP4', '.MOV', '.MKV']:
                src = path
                video = aiopath.AsyncPath(video)
                dst = video.joinpath(path.name)
                await aioshutil.move(src, dst)
            elif path.suffix.upper() in ['.MP3', '.OGG', '.WAV', '.AMR']:
                src = path
                audio = aiopath.AsyncPath(audio)
                dst = audio.joinpath(path.name)
                await aioshutil.move(src, dst)
            elif path.suffix.upper() in ['.ZIP', '.GZ', '.TAR']:
                new_folder = path.parent.joinpath(path.stem)
                if not await new_folder.exists():
                    await new_folder.mkdir()
                try:
                    await aioshutil.unpack_archive(path, new_folder)
                except:
                    print('*' * 100)
                    print(f'{path}')
                    print(f'{path.suffix}')
                    print(f'{path.name}')
                    print('*' * 100)


def normalize(string_to_normalize):
    """
    The function transliterates Cyrillic characters into Latin

    Takes one positional argument, namely a Latin string and other characters.

    Returns a string in Latin characters with unchanged digits, all other characters are replaced with an underscore character.
    """

    #  Checks the entered string for the presence of characters other than those that will undergo transliteration.
    #  Any other characters found are replaced with an underscore character, the rest are retained unchanged.
    full_chars_list = 'абвгдеёжзийклмнопрстуфхъыьэАБВГДЕЁЗИЙКЛМНОПРСТУФХЪЫЬЭ'\
                      'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    map_dict = {}

    new_string = ''
    for char in string_to_normalize:

        if char not in full_chars_list:
            map_dict[ord(char)] = '_'
            new_string += char.translate(map_dict)
            map_dict.clear()
        else:
            new_string += char

    # String to apply transliteration
    string_to_normalize = new_string

    сyrillic_chars = '0123456789абвгдеёжзийклмнопрстуфхъыьэАБВГДЕЁЗИЙКЛМНОПРСТУФХЪЫЬЭ'
    latin_chars = '0123456789abvgde__zijklmnoprstufh_y_eABVGDEEZIJKLMNOPRSTUFH_Y_E'

    # use next one with <.translate>
    correspondence_map = {}

    # create a correspondence_map for <.translate>
    for cyr_char in сyrillic_chars:
        for _ in latin_chars:
            correspondence_map[ord(сyrillic_chars[сyrillic_chars.index(
                cyr_char)])] = latin_chars[сyrillic_chars.index(cyr_char)]
    result = string_to_normalize.translate(correspondence_map)

    return result


async def recursive_del_empty_dir(path):
    """
    The function recursively traverses the entire tree starting
    from the directory specified in the argument and removes all empty folders
    """

    if await path.is_dir():
        async for element in path.iterdir():
            try:
                await element.rmdir()
            except OSError as ex:
                pass
            await recursive_del_empty_dir(element)


async def main():
    try:
        await folder_processing(folder_to_check, images, documents, audio, video)
    except UnboundLocalError as ex:
        print('=' * 75)
        print(
            f'While folder_processing func worked an exception\n{ex} occurred')
    await recursive_del_empty_dir(folder_to_check)


if __name__ == '__main__':
    new_dirs = ['images', 'documents', 'audio', 'video']
    new_dirs_path = input('Enter dir path where to create new dirs: ')

    try:
        images, documents, audio, video = dir_creator(new_dirs, new_dirs_path)
    except TypeError as ex:
        print('=' * 75)
        print(f'Dirs were not created, an exception occurred\n{ex}\n')

    if len(sys.argv) < 2:
        print('You entered more arguments than it has to be. Require only one argument.')
    else:
        path = sys.argv[1]
        folder_to_check = aiopath.AsyncPath(path)

    asyncio.run(main())
