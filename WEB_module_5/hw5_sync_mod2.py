from time import time
from multiprocessing import Pool


def factorize(*number):
    """
    The function takes a list of numbers and returns a list of numbers
    by which the numbers from the input list are divisible without a remainder.
    """
    result = [[i for i in range(1, numb + 1) if numb % i == 0]
              for numb in number]
    return result


if __name__ == '__main__':

    # checking <factorize> function for correct working via <assert> instruction
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    # printing resulting info after function works
    for el in a, b, c, d:
        print(el)
    print()

    # measuring the time spent on the operation of a function
    start_time_synch_factorize = time()

    factorize(128, 255, 99999, 10651060)

    print('=' * 80)
    print(
        f'The synchronous version of the function worked for - {time() - start_time_synch_factorize} seconds')
    print('=' * 80, '\n')
