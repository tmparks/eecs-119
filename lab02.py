#!/usr/bin/env python3

def read_file(file_name):
    """Read words from a file.

    A word is any sequence of non-blank characters.
    """
    with open(file_name) as file:
        for line in file:
            yield from line.split()


def read_sequence(file_name):
    """Read a sequence of integers from a file.

    The sequence in the file is preceded by an integer telling how many elements
    there are in the sequence.
    """
    words = read_file(file_name)  # generator
    length = int(next(words))
    for _ in range(length):
        yield int(next(words))
    words.close()


def two_largest(numbers):
    """Print the two largest different values among a sequence of integers."""
    largest = float('-Infinity')
    next_largest = float('-Infinity')
    for n in numbers:
        if n > largest:  # n is larger
            next_largest = largest
            largest = n
        elif largest > n and n > next_largest:  # n is between
            next_largest = n
    print('Largest value in sequence:', largest)
    print('Next largest value:', next_largest)


two_largest(read_sequence('lab02.txt'))

# Additional test cases.
two_largest([1, 2, 3, 4, 5])
two_largest([5, 4, 3, 2, 1])
two_largest([1, 2, 3, 4, 5, 5, 4, 3, 2, 1])
