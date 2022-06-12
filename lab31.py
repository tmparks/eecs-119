#!/usr/bin/env python3

def new_rabbits(old_rabbits, old_coyotes):
    births = 0.2 * old_rabbits
    starvation_deaths = 0.00002 * old_rabbits * old_rabbits
    other_deaths = old_coyotes * old_rabbits * 45.0 / 10000.0
    return old_rabbits + births - starvation_deaths - other_deaths


def new_coyotes(old_rabbits, old_coyotes):
    births = 0.08 * old_coyotes
    starvation_deaths = old_coyotes * 250.0 / old_rabbits
    return old_coyotes + births - starvation_deaths


def left_pad(spaces, text):
    width = str(spaces + len(text))
    return format(text, '>' + width)


def print_line(month, rabbits, coyotes):
    rabbit_column = round(0.01 * rabbits)
    coyote_column = round(2 * coyotes)
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


# Ten rabbits escape in month 0
rabbits = 10.0
coyotes = 0.0

for month in range(50):
    if month % 3 == 0:
        print_line(month, rabbits, coyotes)
    (rabbits, coyotes) = (new_rabbits(rabbits, coyotes), new_coyotes(rabbits, coyotes))

# Ten coyotes are released 50 months after the first rabbits escaped
coyotes += 10.0

for month in range(50, 301):
    if month % 3 == 0:
        print_line(month, rabbits, coyotes)
    (rabbits, coyotes) = (new_rabbits(rabbits, coyotes), new_coyotes(rabbits, coyotes))

print('In month', month, 'there are', rabbits,
      'rabbits and', coyotes, 'coyotes')
