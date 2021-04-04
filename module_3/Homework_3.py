def fibonacci(n):
    """
    Function for calculating the n-th number in the Fibonacci sequence.

    Takes one positional argument, namely the ordinal number of 
    a number in the Fibonacci sequence.
    """
    if n == 1:
        return 0
    if n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    n = int(input('Enter the ordinal number of the number in the Fibonacci sequence: '))
    result = fibonacci(n)
    print(
        f'The Fibonacci sequence result with the ordinal number - {n} is {result}')


if __name__ == '__main__':
    main()
