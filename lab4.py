#!/usr/bin/env python3

class TextFormatter:
    width = 40        # current line width
    next_width = 40   # line width for next paragraph
    space = 0         # current space between lines
    next_space = 0    # space for next paragraph
    indent = ''       # current indentation
    next_indent = ''  # indentation for next paragraph
    margin = ''       # current margin
    next_margin = ''  # margin for next paragraph
    output = ''       # output line
    first = True      # first line

    def print(self):
        if len(self.output) > 0 and not self.output.isspace():
            print(self.margin + self.output)
            for _ in range(self.space):
                print()  # blank line
            self.output = self.indent
            self.first = False

    def paragraph(self, indent):
        self.print()
        if not self.first:
            print()  # blank line
        self.output += indent
        self.width = self.next_width
        self.space = self.next_space
        self.indent = self.next_indent
        self.margin = self.next_margin

    def argument(self, line, min, max):
        words = line.split()
        assert len(words) == 2
        result = int(words[-1])
        assert min <= result and result <= max
        return result

    def spaces(self, line, min, max):
        n = self.argument(line, min, max)
        return format(' ', '>' + str(n))

    def command(self, line):
        if line.startswith('.PP'):  # new paragraph
            self.paragraph('    ')  # indent
        elif line.startswith('.LP'):
            self.paragraph('')      # no indent
        elif line.startswith('.W'):
            self.next_width = self.argument(line, 30, 99)
        elif line.startswith('.SP'):
            self.next_space = self.argument(line, 0, 9)
        elif line.startswith('.I'):
            self.next_indent = self.spaces(line, 0, 99)
        elif line.startswith('.M'):
            self.next_margin = self.spaces(line, 0, 99)

    def text(self, line):
        for word in line.split():
            if len(self.output) > 0:
                if len(self.output) + len(word) < self.width:
                    self.output += ' '
                else:  # start a new line
                    self.print()
            self.output += word

    def format(self, file_name):
        with open(file_name) as file:
            for line in file:
                if line.startswith('.'):
                    self.command(line)
                else:
                    self.text(line)
            self.print()


f = TextFormatter()
f.format('lab43.txt')
