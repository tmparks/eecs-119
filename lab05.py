#!/usr/bin/env python3
"""
Programming Assignment 5: A simple graphics language
"""


class Plotter:
    """
    A lousy plotter.
    """
    page = []      # page (list of rows)
    off = 0        # number of off-page points
    rows = 0       # number of rows on the page
    columns = 0    # number of columns on the page
    row = 0        # vertical position
    column = 0     # horizontal position
    row_change = 0
    column_change = 0

    def __init__(self, rows, columns):
        """
        Initialize a newly created instance.
        """
        self.rows = rows
        self.columns = columns
        self.erase()

    def move(self, row, column):
        """
        Move the imaginary pen without drawing any output.
        """
        self.row = row
        self.column = column

    def step(self, n):
        """
        Move the imaginary pen, drawing output after each step.
        The new position of the pen is determined by the previously specified
        vertical and horizontal change.
        """
        for _ in range(n):
            self.row += self.row_change
            self.column += self.column_change
            row = round(self.row)
            column = round(self.column)
            if 0 <= row < self.rows and 0 <= column < self.columns:
                line = self.page[row]
                self.page[row] = line[:column] + '*' + line[column+1:]
            else:
                self.off += 1

    def vchange(self, row_change):
        """
        Set the vertical change to the specified number of rows.
        """
        self.row_change = row_change

    def hchange(self, column_change):
        """
        Set the horizontal change to the specified number of columns.
        """
        self.column_change = column_change

    def print(self):
        """
        Print the image.
        """
        print('╭' + '─' * self.columns + '╮')
        for row in reversed(self.page):  # print rows from top to bottom
            print('│' + ''.join(row) + '│')
        print('╰' + '─' * self.columns + '╯')
        if self.off > 0:
            print('There were', self.off, 'off-page points')
            self.off = 0

    def erase(self):
        """
        Erase the image.
        """
        self.page.clear()
        for _ in range(self.rows):
            self.page.append(' ' * self.columns)


def read_words(file_name):
    """
    Read words from a file.

    A word is any sequence of non-blank characters.
    """
    with open(file_name, encoding='utf-8') as file:
        for line in file:
            yield from line.split()


def read_commands(file_name, plotter):
    """
    Read plotting commands from a file.
    """
    words = read_words(file_name)  # generator
    for word in words:
        command = word.lower()  # ignore case
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
read_commands('lab05a.txt', p)
read_commands('lab05b.txt', p)
read_commands('lab05c.txt', p)
read_commands('lab05d.txt', p)
read_commands('lab05e.txt', p)
