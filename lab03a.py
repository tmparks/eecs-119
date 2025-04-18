#!/usr/bin/env python3
"""
Programming Assignment 3: A simulation of a predator prey system
"""


def new_rabbits(old_rabbits, old_coyotes):
    """
    Number of rabbits alive in a new month
    given the number of rabbits and coyotes alive in the previous month.
    """
    births = 2e-1 * old_rabbits
    starvation_deaths = 2e-5 * old_rabbits * old_rabbits
    other_deaths = old_coyotes * old_rabbits * 4.5e-3
    return old_rabbits + births - starvation_deaths - other_deaths


def new_coyotes(old_rabbits, old_coyotes):
    """
    Number of coyotes alive in a new month
    given the number of rabbits and coyotes alive in the previous month.
    """
    births = 8e-2 * old_coyotes
    starvation_deaths = old_coyotes * 2.5e2 / old_rabbits
    return old_coyotes + births - starvation_deaths


def small_change(old, new):
    """
    Determine if a change is smaller than 1%
    """
    return abs(new - old) < 1e-2 * abs(old)


def update(old_rabbits, old_coyotes):
    """
    Update rabbit and coyote populations.
    """
    rabbits = new_rabbits(old_rabbits, old_coyotes)
    coyotes = new_coyotes(old_rabbits, old_coyotes)
    stop = (small_change(old_rabbits, rabbits)
            and small_change(old_coyotes, coyotes))
    return (stop, rabbits, coyotes)


def print_line(month, rabbits, coyotes):
    """
    Print one line of a graphical display of rabbit and coyote populations.
    """
    if month % 3 != 0:
        return
    rabbit_column = round(1e-2 * rabbits)
    coyote_column = round(2.0 * coyotes)
    if rabbit_column < coyote_column:
        left = 'r'.rjust(rabbit_column + 1)
        right = 'c'.rjust(coyote_column - rabbit_column)
    elif coyote_column < rabbit_column:
        left = 'c'.rjust(coyote_column + 1)
        right = 'r'.rjust(rabbit_column - coyote_column)
    else:  # print only r when equal
        left = 'r'.rjust(rabbit_column + 1)
        right = ''
    print(format(month, '3') + '|' + left + right)


def test():
    """
    Test cases.
    """
    rabbits = 10.0  # Ten rabbits escape in month 0
    coyotes = 0.0

    for month in range(300):
        if month == 50:
            coyotes += 10.0  # Ten coyotes are released in month 50
        print_line(month, rabbits, coyotes)
        (stop, rabbits, coyotes) = update(rabbits, coyotes)
        if stop:
            break
    month += 1

    print_line(month, rabbits, coyotes)

    print('In month', month, 'there are',
          rabbits, 'rabbits and', coyotes, 'coyotes')


test()
