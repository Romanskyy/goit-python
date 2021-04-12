import sys
from pathlib import Path

# create lists to collect info after function works
images = []
video_files = []
documents = []
music = []
archives = []
known_extensions = []
unknown_extensions = []


def folder_processing(path):

    
    """
    The function goes to the maximum nesting depth of the specified
    folder and sorts the files by type.

    Takes one argument, namely the directory path,
    as an argument when called from the command line.

    path: full path to the folder for working with one
    """


    if path.exists():
        if path.is_dir():
            for element in path.iterdir():
                folder_processing(element)
        else:
            if path.suffix.upper() in ['.JPEG', '.PNG', '.JPG', '.SVG']:
                images.append(path.name)
                known_extensions.append(path.suffix.upper())
            elif path.suffix.upper() in ['.AVI', '.MP4', '.MOV', '.MKV']:
                video_files.append(path.name)
                known_extensions.append(path.suffix.upper())
            elif path.suffix.upper() in ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']:
                documents.append(path.name)
                known_extensions.append(path.suffix.upper())
            elif path.suffix.upper() in ['.MP3', '.OGG', '.WAV', '.AMR']:
                music.append(path.name)
                known_extensions.append(path.suffix.upper())
            elif path.suffix.upper() in ['.ZIP', '.GZ', '.TAR']:
                archives.append(path.name)
                known_extensions.append(path.suffix.upper())
            else:
                unknown_extensions.append(path.suffix.upper())
    else:
        print(f'Entered data {path} is not a path to folder for checking')
    return images, video_files, documents, music, archives, list(set(known_extensions)), list(set(unknown_extensions))


def main():
    if len(sys.argv) < 2:
        print('You entered more arguments than it has to be. Require only one argument.')
    else:
        path = sys.argv[1]
        folder_to_check = Path(path)
        images, video_files, documents, music, archives, known_extensions, unknown_extensions = folder_processing(
            folder_to_check)

        if len(images) > 0:
            print(f'\nList of images\n{"-" * 100}\n{images}\n{"-" * 100}\n')

        if len(video_files) > 0:
            print(
                f'List of video files\n{"-" * 100}\n{video_files}\n{"-" * 100}\n')

        if len(documents) > 0:
            print(
                f'List of documents\n{"-" * 100}\n{documents}\n{"-" * 100}\n')

        if len(music) > 0:
            print(f'List of music\n{"-" * 100}\n{music}\n{"-" * 100}\n')

        if len(archives) > 0:
            print(f'List of arc\n{"-" * 100}\n{archives}\n{"-" * 100}\n')

        if len(known_extensions) > 0:
            print(
                f'List of known extensions\n{"-" * 100}\n{known_extensions}\n{"-" * 100}\n')

        if len(unknown_extensions) > 0:
            print(
                f'List of unknown extensions\n{"-" * 100}\n{unknown_extensions}\n{"-" * 100}')


if __name__ == '__main__':
    main()
