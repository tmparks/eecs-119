#!/usr/bin/env python3

def new_rabbits(old_rabbits, old_coyotes):
    births = 2e-1 * old_rabbits
    starvation_deaths = 2e-5 * old_rabbits * old_rabbits
    other_deaths = old_coyotes * old_rabbits * 4.5e-3
    return old_rabbits + births - starvation_deaths - other_deaths


def new_coyotes(old_rabbits, old_coyotes):
    births = 8e-2 * old_coyotes
    starvation_deaths = old_coyotes * 2.5e2 / old_rabbits
    return old_coyotes + births - starvation_deaths


def small_change(old, new):
    return old != 0.0 and abs((new - old) / old) < 1e-2


def update(old_rabbits, old_coyotes):
    rabbits = new_rabbits(old_rabbits, old_coyotes)
    coyotes = new_coyotes(old_rabbits, old_coyotes)
    stop = (small_change(old_rabbits, rabbits)
            and small_change(old_coyotes, coyotes))
    return (stop, rabbits, coyotes)


def left_pad(spaces, text):
    width = str(spaces + len(text))
    return format(text, '>' + width)


def print_line(month, rabbits, coyotes):
    if month % 3 != 0:
        return
    rabbit_column = round(1e-2 * rabbits)
    coyote_column = round(2.0 * coyotes)
    left = ''
    right = ''
    if rabbit_column < coyote_column and rabbits > 0.0:
        left = left_pad(rabbit_column, 'r')
        right = left_pad(coyote_column - rabbit_column - 1, 'c')
    elif coyote_column < rabbit_column and coyotes > 0.0:
        left = left_pad(coyote_column, 'c')
        right = left_pad(rabbit_column - coyote_column - 1, 'r')
    elif rabbits > 0.0:
        left = left_pad(rabbit_column, 'r')
    print(format(month, '3') + '|' + left + right)


rabbits = 10.0 # Ten rabbits escape in month 0
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
