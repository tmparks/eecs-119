#!/usr/bin/env python3

class TextFormatter:
    width = 40       # current line width
    next_width = 40  # line width for next paragraph
    output = ''      # output line
    first = True     # first paragraph

    def print(self):
        if len(self.output) > 0:
            print(self.output)
        self.output = ''

    def paragraph(self, indent):
        if not self.first:
            self.print()
            print()  # blank line
        self.output = indent
        self.width = self.next_width

    def command(self, line):
        if line.startswith('.PP'):  # new paragraph
            self.paragraph('    ')  # indent
        elif line.startswith('.LP'):
            self.paragraph('')      # no indent
        elif line.startswith('.W'):
            self.next_width = int(line.split()[-1])
            assert 30 <= self.next_width and self.next_width <= 99

    def text(self, line):
        for word in line.split():
            if len(self.output) > 0:
                if len(self.output) + len(word) < self.width:
                    self.output += ' '
                else:  # start a new line
                    self.print()
            self.output += word
        self.first = False

    def format(self, file_name):
        with open(file_name) as file:
            for line in file:
                if line.startswith('.'):
                    self.command(line)
                else:
                    self.text(line)
            self.print()


f = TextFormatter()
f.format('lab42.txt')
