# Programming Assignment 1
## Part Two

Write a program that reads a sequence of integers from a file and prints the two
largest different values among them. Your program should assume that the
sequence of integers is preceded by another integer telling how many elements
there are in the sequence. Thus when given the input:

    7 1 -3 6 4 3 6 5

your program should produce the following output

    Largest value in the sequence: 6
    Next largest value: 5

This is because the initial seven just tells that there are seven numbers
following it (note that the second six was ignored: we want the two largest
different values).

You can assume that there will be at least two different values among the
numbers in the sequence, that is, an input like

    5 4 4 4 4 4

will not occur.
