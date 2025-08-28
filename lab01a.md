# Programming Assignment 1
## Part One

Write a program that computes the following two sums:

    1E12 + 1/1 + 1/2 + 1/3 + ... + 1/999 + 1/1000 - 1E12

and

    1/1 + 1/2 + 1/3 + ... + 1/999 + 1/1000

The sums should be computed from left to right, that is, adding the second term
to the first, the third to the resulting sum, the fourth to the new sum, and so
on.

Clearly the values of the two sums ought to be identical but you will discover
that they are not. This is due to the fact that real numbers are kept with a
finite precision. The representation of real numbers in a computer and some of
the problems that it causes will be the topic of one of your precepts.
