#!/usr/bin/env python3
"""
Programming Assignment 3: A simple interactive game
"""


def them(stones, start):
    """
    Human takes a turn.
    """
    print('There are', stones, 'stones')
    while True:
        take = int(input('How many do you take? '))
        if take == 0 and stones == start:
            print('In that case I will go first')
            break
        elif take < 1:
            print('You must take a stone')
        elif take > 3:
            print('You cannot take more than 3 stones')
        elif take > stones:
            print('There are only', stones, 'stones')
        else:
            break
    return take


def us(stones):
    """
    Computer takes a turn.
    """
    take = max(1, (stones - 1) % 4)  # must take at least one
    print('I take', take)
    return take


def play():
    """
    Play the game.
    """
    start = 21
    stones = start

    while stones > 0:
        stones -= them(stones, start)
        if stones == 0:
            print('You took the last stone. You lose.')
        else:
            stones -= us(stones)
            if stones == 0:
                print('I took the last stone. I lose.')


play()
