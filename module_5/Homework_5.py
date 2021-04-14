def normalize(string_to_normalize):

    """
    The function transliterates Cyrillic characters into Latin

    Takes one positional argument, namely a Latin string and other characters.

    Returns a string in Latin characters with unchanged digits, all other characters are replaced with an underscore character.
    """

    #  Checks the entered string for the presence of characters other than those that will undergo transliteration. 
    #  Any other characters found are replaced with an underscore character, the rest are retained unchanged.
    full_chars_list = 'абвгдеёжзийклмнопрстуфхъыьэАБВГДЕЁЗИЙКЛМНОПРСТУФХЪЫЬЭ'\
                      'abvgdezijklmnoprstufhyeABVGDEEZIJKLMNOPRSTUFHYE0123456789'

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

    # for general understanding
    # clear_map_chars = {}

    # create a correspondence_map for <.translate>
    for cyr_char in сyrillic_chars:
        for _ in latin_chars:
            correspondence_map[ord(сyrillic_chars[сyrillic_chars.index(
                cyr_char)])] = latin_chars[сyrillic_chars.index(cyr_char)]
            # clear_map_chars[сyrillic_chars[сyrillic_chars.index(cyr_char)]] = latin_chars[сyrillic_chars.index(cyr_char)]
    result = string_to_normalize.translate(correspondence_map)

    return result


def main():
    asked_string = input('Enter a string for transliteration:\n')
    result = normalize(asked_string)
    return result


if __name__ == '__main__':
    clear_string = main()
    print(clear_string)
