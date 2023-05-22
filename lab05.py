#!/usr/bin/env python3

class Plotter:
    page = list()  # page (list of rows)
    off = 0        # number of off-page points
    rows = 0       # number of rows on the page
    columns = 0    # number of columns on the page
    row = 0        # vertical position
    column = 0     # horizontal position
    row_change = 0
    column_change = 0

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.erase()

    def move(self, row, column):
        self.row = row
        self.column = column

    def step(self, n):
        for _ in range(n):
            self.row += self.row_change
            self.column += self.column_change
            row = round(self.row)
            column = round(self.column)
            if (0 <= row and row < self.rows
                    and 0 <= column and column < self.columns):
                line = self.page[row]
                self.page[row] = line[:column] + '*' + line[column+1:]
            else:
                self.off += 1

    def vchange(self, row_change):
        self.row_change = row_change

    def hchange(self, column_change):
        self.column_change = column_change

    def print(self):
        print('╭' + '─' * self.columns +'╮')
        for row in reversed(self.page): # print rows from top to bottom
            print('│' + ''.join(row) + '│')
        print('╰' + '─' * self.columns + '╯')
        if (self.off > 0):
            print('There were', self.off, 'off-page points')
            self.off = 0

    def erase(self):
        self.page.clear()
        for _ in range(self.rows):
            self.page.append(' ' * self.columns)


def read_words(file_name):
    """
    Read words from a file.

    A word is any sequence of non-blank characters.
    """
    with open(file_name) as file:
        for line in file:
            yield from line.split()

def read_commands(file_name, plotter):
    words = read_words(file_name) # generator
    for word in words:
        command = word.lower() # ignore case
        if command.startswith('m'):
            row = float(next(words))
            column = float(next(words))
            plotter.move(row, column)
        elif command.startswith('s'):
            count = int(next(words))
            plotter.step(count)
        elif command.startswith('v'):
            change = float(next(words))
            plotter.vchange(change)
        elif command.startswith('h'):
            change = float(next(words))
            plotter.hchange(change)
        elif command.startswith('p'):
            plotter.print()
        elif command.startswith('e'):
            plotter.erase()
        else:
            print('Unrecognized command ' + command)


p = Plotter(rows=56, columns=130)
read_commands('lab51.txt', p)
read_commands('lab52.txt', p)
read_commands('lab53.txt', p)
read_commands('lab54.txt', p)
read_commands('lab55.txt', p)
