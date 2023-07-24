#!/usr/bin/env python3

class Picture:
    light = +1  # initial value for light pixels
    dark = -1   # initial value for dark pixels
    lines = 0   # number of lines in picture
    columns = 0 # number of columns in picture
    light_regions = 0 # number of light regions
    dark_regions = 0  # number of dark regions
    light_edge_regions = set() # colors for light regions that touch the edge
    dark_edge_regions = set()  # colors for dark regions that touch the an edge
    region_sizes = dict() # sizes of regions
    picture = list()      # picture (list of lines)

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

    def print(self, min, max):
        print(self.lines)
        print(self.columns)
        for line in self.picture:
            for pixel in line:
                if pixel <= self.dark and min <= self.region_sizes[pixel] and self.region_sizes[pixel] <= max:
                    print('*', end='')
                else:
                    print('-', end='')
            print()

    def color(self):
        for l in range(self.lines):
            for c in range(self.columns):
                if self.picture[l][c] == self.light:
                    self.light_regions += 1
                    color = self.light + self.light_regions
                    self.region_sizes[color] = self.flood(l, c, self.light, color)
                elif self.picture[l][c] == self.dark:
                    self.dark_regions += 1
                    color = self.dark - self.dark_regions
                    self.region_sizes[color] = self.flood(l, c, self.dark, color)
                self.check_edge(l, c)

    def flood(self, l, c, old_color, new_color):
        size = 0
        if (0 <= l and l < self.lines
            and 0 <= c and c < self.columns
            and self.picture[l][c] == old_color):
            self.picture[l][c] = new_color
            size += 1
            size += self.flood(l+1, c, old_color, new_color)
            size += self.flood(l-1, c, old_color, new_color)
            size += self.flood(l, c+1, old_color, new_color)
            size += self.flood(l, c-1, old_color, new_color)
            # self.flood(l+1, c+1, old_color, new_color)
            # self.flood(l+1, c-1, old_color, new_color)
            # self.flood(l-1, c+1, old_color, new_color)
            # self.flood(l-1, c-1, old_color, new_color)
        return size

    def check_edge(self, l, c):
        if l == 0 or c == 0 or l == self.lines - 1 or c == self.columns - 1:
            if self.picture[l][c] >= self.light:
                self.light_edge_regions.add(self.picture[l][c])
            if self.picture[l][c] <= self.dark:
                self.dark_edge_regions.add(self.picture[l][c])

def test():
    p = Picture()
    p.read('lab07a.txt')
    p.color()
    p.print(1, 100*100)
    print('There are', p.light_regions, 'light regions.')
    print(len(p.light_edge_regions), 'touch an edge')
    print('There are', p.dark_regions, 'dark regions')
    print(len(p.dark_edge_regions), 'touch an edge')
    print('Regions with 1 to 20 pixels')
    p.print(1, 20)
    print('Regions with 21 to 40 pixels')
    p.print(21, 40)
    print('Regions with 41 to 80 pixels')
    p.print(41, 80)
    print('Regions with more than 80 pixels')
    p.print(80, 100*100)
test()
