#!/usr/bin/env python3

def read_file(file_name):
    """Read words from a file.

    A word is any sequence of non-blank characters.
    """
    with open(file_name) as file:
        for line in file:
            yield from line.split()


def print_words(file_name):
    """Read a sequence of words from a file and print them.

    Line breaks in the input are ignored.
    One blank is printed between two words on the same line.
    A new line is started after any word that starts with r, s, or t.
    Stops when the character % is encountered.
    A word is any sequence of non-blank characters except %.
    """
    line = []
    for word in read_file(file_name):
        if word.startswith('%'):
            break
        line.append(word.strip('%'))
        if (word.startswith(('r', 's', 't'))):
            print(' '.join(line))
            line.clear()
        if word.endswith('%'):
            break
    if len(line) > 0:
        print(' '.join(line))


print_words('lab03.txt')
