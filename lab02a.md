# Programming Assignment 2
## Part One

Write a program that reads a file containing text and writes one number for each
line of text according to the rules given below. In these rules "word" means any
sequence of consecutive non-blank characters.

1.  The output text should consist of the same number of lines as the input
    text.
2.  Each line of the output contains the number of characters in the longest
    word on that line of the input.
3.  If any line of the input text is blank, the progran may crash in a merciless
    fashion.

To illustrate, if the input file contains:

    Just some silly text an example of
    what your program is supposed to do.
    More:
    so you know what to do with it.

the program should produce the following output:

    7
    8
    5
    4
