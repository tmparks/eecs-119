#!/usr/bin/env python3
"""
Programming Assignment 6: Strange function
"""


def f(x):
    """
    A strange function.
    """
    if x > 100:
        return x - 10
    else:
        return g(f(x + 11))


def g(x):
    """
    Another strange function.
    """
    if x > 100:
        return x - 10
    else:
        return f(g(x + 11))


def test():
    """
    Test cases.
    """
    for x in range(200):
        print('f(' + str(x) + ') =', f(x))

# test()


print('on what input would you like me to run the function')
arg = input()
print('f(' + arg + ') =', f(int(arg)))
