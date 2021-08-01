from time import time
from multiprocessing import Pool


def factorize(number):
    """
    The function takes a number and returns a list of numbers
    by which the number from the input are divisible without a remainder.
    """
    result = [i for i in range(1, number + 1) if number % i == 0]
    return result


if __name__ == '__main__':

    numbers = [128, 255, 99999, 10651060]

    # checking <factorize> function for correct working via <assert> instruction
    for_assert = []
    for numb in numbers:
        for_assert.append(factorize(numb))

    a, b, c, d = for_assert

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    # printing resulting info after function works
    for el in for_assert:
        print(el)
    print()

    # measuring the time spent on the operation of a function with a different number of running processes
    proces_amount = 1

    while proces_amount < 5:

        start_time_asynch_factorize = time()

        with Pool(processes=proces_amount) as pool:
            list(pool.map(factorize, numbers))

        print('=' * 80)
        print(
            f'The asynchronous version of the function worked for - {time() - start_time_asynch_factorize} seconds,\nprocesses used - {proces_amount}.')
        print('=' * 80, '\n')

        proces_amount += 1
