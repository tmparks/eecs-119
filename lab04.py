#!/usr/bin/env python3
"""
Programming Assignment 4: Text formatter
"""


class TextFormatter:
    """
    A simple text formatter.
    """
    width = 40               # current line width limit
    next_width = 40          # line width limit for next paragraph
    space = 0                # current space between lines
    next_space = 0           # space for next paragraph
    indent = ''              # current indentation
    next_indent = ''         # indentation for next paragraph
    margin = ''              # current margin
    next_margin = ''         # margin for next paragraph
    do_format = True         # current formatting state
    do_justify = False       # current justification state
    next_do_justify = False  # justification for the next paragraph
    output = ''              # output line
    words = list()           # words in current line
    is_first_line = True     # first line

    def print_line(self, justify):
        """
        Print a line of text (with optional justification)
        """
        if len(self.words) > 0:
            gaps = len(self.words) - 1
            length = len(self.output) + sum(len(word) for word in self.words)
            total = length + gaps  # default is one space per gap
            if justify:
                total = len(self.margin) + self.width
            remaining_pad = total - length
            for n in range(gaps):
                remaining_gaps = gaps - n
                pad = round(remaining_pad / remaining_gaps)
                width = pad + len(self.words[n])
                self.output += self.words[n].ljust(width)
                remaining_pad -= pad
            self.output += self.words[-1]  # last word
            print(self.output)
            for _ in range(self.space):
                print()  # blank line
            self.output = self.margin + self.indent
            self.words.clear()
            self.is_first_line = False

    def paragraph(self, indent):
        """
        Process a paragraph.
        """
        self.print_line(False)  # last line is never justified
        if not self.is_first_line:
            print()  # blank line
        self.width = self.next_width
        self.space = self.next_space
        self.indent = self.next_indent
        self.margin = self.next_margin
        self.do_justify = self.next_do_justify
        self.output = self.margin + self.indent + indent

    def label(self, width, words):
        """
        Process a paragraph label.
        """
        label = ' '.join(words)
        if label.startswith('<'):
            label = label[1:]
        if label.endswith('>'):
            label = label[:-1]
        if len(label) >= width:
            label += ' '
        return label.ljust(width)

    def command(self, line):
        """
        Process a command.
        """
        args = line.split()
        if args[0] == '.PP':         # new paragraph
            self.paragraph(5 * ' ')  # indent
        elif args[0] == '.LP':
            self.paragraph('')       # no indent
        elif args[0] == '.IP':
            self.next_indent = int(args[1]) * ' '
            self.paragraph('')       # no additional indent
            self.output = self.margin + self.label(len(self.indent), args[2:])
        elif args[0] == '.W':
            self.next_width = int(args[1])
        elif args[0] == '.SP':
            self.next_space = int(args[1])
        elif args[0] == '.I':
            self.next_indent = int(args[1]) * ' '
        elif args[0] == '.M':
            self.next_margin = int(args[1]) * ' '
        elif args[0] == '.JST':
            self.next_do_justify = True
        elif args[0] == '.NJST':
            self.next_do_justify = False
        elif args[0] == '.NF':
            self.print_line(False)  # last line is never justified
            self.do_format = False
        elif args[0] == '.FI':
            self.do_format = True
        else:
            pass  # ignore unrecognized commands

    def text(self, line):
        """
        Process a line of text.
        """
        length = (len(self.output)
                  + sum(len(word) for word in self.words)
                  + len(self.words))
        limit = len(self.margin) + self.width
        for word in line.split():
            if length + len(word) > limit:
                self.print_line(self.do_justify)
                length = len(self.output)
            self.words.append(word)
            length += len(word) + 1  # allow for space between words

    def format(self, file_name):
        """
        Produce formatted output from a text file with embeddd commands.
        """
        with open(file_name, encoding='utf-8') as file:
            for line in file:
                if not self.do_format and not line.startswith('.FI'):
                    print(line, end='')
                elif line.startswith('.'):
                    self.command(line)
                else:
                    self.text(line)
            self.print_line(False)  # last line is never justified


def test():
    """
    Test cases.
    """
    print('1234567890123456789012345678901234567890')
    f = TextFormatter()
    f.format('lab04a.txt')
    f.format('lab04b.txt')
    f.format('lab04c.txt')
    f.format('lab04d.txt')
    f.format('lab04e.txt')


test()
