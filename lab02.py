#!/usr/bin/env python3

def two_largest(numbers):
    largest = float('-Infinity')
    next_largest = float('-Infinity')
    for n in numbers:
        if n >= largest:
            largest = n
        elif n > next_largest:
            next_largest = n
    print('Largest value in sequence:', largest)
    print('Next largest value:', next_largest)


def read_file(file_name):
    with open(file_name) as f:
        result = []
        for line in f:
            result.extend(line.split())
    return result


def read_sequence(file_name):
    result = [int(x) for x in read_file(file_name)]
    assert result[0] == len(result) - 1
    return result[1:]


two_largest(read_sequence('lab02.txt'))
