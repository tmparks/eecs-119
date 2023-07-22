#!/usr/bin/env python3

class Picture:
    light = 0        # value for light pixels
    dark = -1        # value for dark pixels
    lines = 0        # number of lines in picture
    columns = 0      # number of columns in picture
    picture = list() # picture (list of lines)

    def erase(self, lines, columns):
        self.lines = lines
        self.columns = columns
        self.picture = list()
        for l in range(lines):
            line = list()
            for c in range(columns):
                line.append(self.light)
            self.picture.append(line)

    def read(self, file_name):
        with open(file_name) as file:
            lines = int(next(file))
            columns = int(next(file))
            self.erase(lines, columns)
            for l in range(lines):
                line = next(file)
                for c in range(columns):
                    if line[c] == '*':
                        self.picture[l][c] = self.dark

    def print(self):
        print(self.lines)
        print(self.columns)
        for line in self.picture:
            for pixel in line:
                if pixel == self.light:
                    print('-', end='')
                else:
                    print('*', end='')
            print()

def test():
    p = Picture()
    p.read('lab07a.txt')
    p.print()

test()
