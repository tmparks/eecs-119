#!/usr/bin/env python3

def read_file(file_name):
    with open(file_name) as f:
        for line in f:
            for word in line.split():
                yield word


def print_words(file_name):
    line = []
    for word in read_file(file_name):
        line.append(word.strip('%'))
        if (word.startswith(('r', 's', 't'))):
            print(' '.join(line))
            line.clear()
    if len(line) > 0:
        print(' '.join(line))


print_words('lab03.txt')
