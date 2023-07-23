#!/usr/bin/env python3

class Picture:
    light = +1        # value for light pixels
    dark = -1         # value for dark pixels
    lines = 0         # number of lines in picture
    columns = 0       # number of columns in picture
    light_regions = 0 # number of light regions
    dark_regions = 0  # number of dark regions
    picture = list()  # picture (list of lines)

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
                if pixel >= self.light:
                    print('-', end='')
                else:
                    print('*', end='')
            print()

    def color(self):
        for l in range(self.lines):
            for c in range(self.columns):
                if self.picture[l][c] == self.light:
                    self.light_regions += 1
                    self.flood(l, c, self.light, self.light + self.light_regions)
                elif self.picture[l][c] == self.dark:
                    self.dark_regions += 1
                    self.flood(l, c, self.dark, self.dark - self.dark_regions)

    def flood(self, l, c, old_color, new_color):
        if (0 <= l and l < self.lines
            and 0 <= c and c < self.columns
            and self.picture[l][c] == old_color):
            self.picture[l][c] = new_color
            self.flood(l+1, c, old_color, new_color)
            self.flood(l-1, c, old_color, new_color)
            self.flood(l, c+1, old_color, new_color)
            self.flood(l, c-1, old_color, new_color)
            # self.flood(l+1, c+1, old_color, new_color)
            # self.flood(l+1, c-1, old_color, new_color)
            # self.flood(l-1, c+1, old_color, new_color)
            # self.flood(l-1, c-1, old_color, new_color)

def test():
    p = Picture()
    p.read('lab07a.txt')
    p.color()
    p.print()
    print('There are', p.light_regions, 'light regions')
    print('There are', p.dark_regions, 'dark regions')

test()
