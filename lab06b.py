#!/usr/bin/env python3

def is_safe(position, queens):
    """
    Test the safety of placing a queen in the given position
    taking into account the given positions of other queens.
    """
    (row, col) = position
    for (occupied_row, occupied_col) in queens:
        if (row == occupied_row
            or col == occupied_col
            or abs(row - occupied_row) == abs(col - occupied_col)):
            return False
    return True


def solve(n):
    """
    Attempt to place N queens on an NxN board.
    Place each queen in the first available safe position.
    Returns a list of up to N positions.
    """
    queens = list()
    for row in range(n):
        for col in range(n):
            position = (row, col)
            if is_safe(position, queens):
                queens.append(position)
                break # cannot place additional queens in same row
    return queens


def test():
    for n in range(1, 8):
        queens = solve(n)
        print('placed', len(queens), 'queens on', n, 'x', n, 'board')
        print(queens)

test()
