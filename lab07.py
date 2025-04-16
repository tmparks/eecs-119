#!/usr/bin/env python3
"""
Programming Assignment 7: Scene analysis
"""


class Picture:
    """
    A simple picture.
    """
    light = +1   # initial value for light pixels
    dark = -1    # initial value for dark pixels
    neutral = 0  # temporary value for pixels
    lines = 0    # number of lines in picture
    columns = 0  # number of columns in picture
    light_regions = set()  # colors of light regions
    dark_regions = set()   # colors of dark regions
    light_edge_regions = set()  # colors of light regions that touch the edge
    dark_edge_regions = set()   # colors of dark regions that touch the an edge
    region_sizes = dict()  # sizes of regions
    picture = list()       # picture (list of lines)

    def erase(self, lines, columns):
        """
        Resize the picture to the given number of lines and columns,
        and set all pixels to the light value.
        """
        self.lines = lines
        self.columns = columns
        self.picture = list()
        for _ in range(lines):
            line = list()
            for _ in range(columns):
                line.append(self.light)
            self.picture.append(line)

    def read(self, file_name):
        """
        Read a picture from a file.
        The first number read specifies the number of lines.
        The second number read specifies the number of columns.
        The '*' character indicates a dark pixel.
        The '-' character indicates a light pixel.
        """
        with open(file_name, encoding='utf-8') as file:
            lines = int(next(file))
            columns = int(next(file))
            self.erase(lines, columns)
            for row in range(lines):
                line = next(file)
                for col in range(columns):
                    if line[col] == '*':
                        self.picture[row][col] = self.dark

    def print(self, dark_regions):
        """
        Print the picture.
        Only dark regions with the given pixel values are printed.
        The '*' character indicates a dark pixel.
        The '-' character indicates a light pixel.
        """
        for line in self.picture:
            for pixel in line:
                if pixel in dark_regions:
                    print('*', end='')
                else:
                    print('-', end='')
            print()

    def color(self):
        """
        Color the picture.
        Replace dark pixels with negative values.
        Replace light pixels with positive values.
        Each dark or light region is assigned a unique pixel value.
        The size of each region is saved.
        The sets of pixel values for light and dark regions,
        as well as for edge-touching regions, are also saved.
        """
        for row in range(self.lines):
            for col in range(self.columns):
                if self.picture[row][col] == self.light:
                    color = self.light + len(self.light_regions) + 1
                    self.light_regions.add(color)
                    self.region_sizes[color] = self.flood(
                        row, col, self.light, color)
                elif self.picture[row][col] == self.dark:
                    color = self.dark - len(self.dark_regions) - 1
                    self.dark_regions.add(color)
                    self.region_sizes[color] = self.flood(
                        row, col, self.dark, color)
                self.check_edge(row, col)

    def flood(self, row, col, old_color, new_color):
        """
        Recursively color a region by filling the pixel in the given
        line and column as well its four nearest neighbors with a new color.
        Returns the number of pixels in the region.
        """
        size = 0
        if (
                0 <= row < self.lines
                and 0 <= col < self.columns
                and self.picture[row][col] == old_color):
            self.picture[row][col] = new_color
            size += 1
            size += self.flood(row+1, col, old_color, new_color)
            size += self.flood(row-1, col, old_color, new_color)
            size += self.flood(row, col+1, old_color, new_color)
            size += self.flood(row, col-1, old_color, new_color)
        return size

    def check_edge(self, row, col):
        """
        Check whether or not the pixel in the given line and column
        is on the edge of the image.
        The sets of pixel values for light and dark edge-touching regions
        are updated accordingly.
        """
        if (
                row == 0
                or col == 0
                or row == self.lines - 1
                or col == self.columns - 1):
            color = self.picture[row][col]
            if color >= self.light:
                self.light_edge_regions.add(color)
            if color <= self.dark:
                self.dark_edge_regions.add(color)

    def neighbors(self, row, col, color):
        """
        Returns the set of pixel values for regions that neighbor
        the region of the given line, column, and color.
        The color of pixels in the region is changed to neutral.
        The caller is responsible for restoring the original color
        of the region by calling flood().
        """
        result = set()
        if 0 <= row < self.lines and 0 <= col < self.columns:
            if self.picture[row][col] == color:
                self.picture[row][col] = self.neutral
                result.update(self.neighbors(row+1, col, color))
                result.update(self.neighbors(row-1, col, color))
                result.update(self.neighbors(row, col+1, color))
                result.update(self.neighbors(row, col-1, color))
            elif self.picture[row][col] != self.neutral:
                result.add(self.picture[row][col])
        return result

    def surrounded(self):
        """
        Returns the set of pixel values for dark regions that are completely
        surrounded by other dark regions.
        Note that such a dark region must neighbor only light regions that
        do not touch an edge.
        """
        result = set()
        light_regions = self.light_regions - self.light_edge_regions
        dark_regions = self.dark_regions - self.dark_edge_regions
        for row in range(self.lines):
            for col in range(self.columns):
                color = self.picture[row][col]
                if color in dark_regions:
                    if self.neighbors(row, col, color).issubset(light_regions):
                        result.add(color)
                    self.flood(row, col, self.neutral, color)
        return result

    def regions_by_size(self, regions, min_size, max_size):
        """
        Returns the set of pixel values for regions that have a size
        between the given bounds.
        """
        result = set()
        for color in regions:
            size = self.region_sizes[color]
            if min_size <= size <= max_size:
                result.add(color)
        return result


def test():
    """
    Test cases.
    """
    p = Picture()
    p.read('lab07.txt')
    p.color()
    p.print(p.dark_regions)
    print('There are', len(p.light_regions), 'light regions.')
    print(len(p.light_edge_regions), 'touch an edge')
    print('There are', len(p.dark_regions), 'dark regions')
    print(len(p.dark_edge_regions), 'touch an edge')
    print('Regions with 1 to 20 pixels')
    p.print(p.regions_by_size(p.dark_regions, 1, 20))
    print('Regions with 21 to 40 pixels')
    p.print(p.regions_by_size(p.dark_regions, 21, 40))
    print('Regions with 41 to 80 pixels')
    p.print(p.regions_by_size(p.dark_regions, 41, 80))
    print('Regions with more than 80 pixels')
    p.print(p.regions_by_size(p.dark_regions, 80, 100*100))
    print('Surrounded regions')
    p.print(p.surrounded())


test()
