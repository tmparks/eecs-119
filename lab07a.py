#!/usr/bin/env python3

def new_picture(lines, columns):
    picture = list()
    for l in range(lines):
        line = list()
        for c in range(columns):
            line.append(0)
        picture.append(line)
    return picture

def read_picture(file_name):
    with open(file_name) as file:
        lines = int(next(file))
        columns = int(next(file))
        picture = new_picture(lines, columns)
        for l in range(lines):
            line = next(file)
            for c in range(columns):
                if line[c] == '*':
                    picture[l][c] = 1
    return picture

def print_picture(picture):
    print(len(picture))
    print(len(picture[0]))
    for line in picture:
        for pixel in line:
            if pixel == 0:
                print('-', end='')
            else:
                print('*', end='')
        print()

def test():
    picture = read_picture('lab07a.txt')
    print_picture(picture)

test()
