#!/usr/bin/env python3

def read_words(file_name):
    """
    Read words from a file.

    A word is any sequence of non-blank characters.
    Line breaks in the input are discarded.
    Stops when the character % is encountered.
    """
    with open(file_name) as file:
        for line in file:
            (line, eof, _) = line.partition('%')
            yield from line.split()
            if eof:  # found end-of-file character
                break


def print_words(file_name):
    """
    Read a sequence of words from a file and print them.

    One blank is printed between two words on the same line.
    A new line is started after any word that starts with r, s, or t.
    """
    line = []
    for word in read_words(file_name):
        line.append(word)
        if (word.startswith(('r', 's', 't'))):
            print(' '.join(line))
            line.clear()
    if line:
        print(' '.join(line))


print_words('lab03.txt')
