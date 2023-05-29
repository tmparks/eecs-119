#!/usr/bin/env python3

def longest_word(file_name):
    """
    Reads lines from a file and prints the length of the longest word
    for each line.
    """
    with open(file_name) as file:
        for line in file:
            print(max(len(word) for word in line.split()))


longest_word('lab02a.txt')
