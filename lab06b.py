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


def solve_recursively(n, row, queens):
    """
    Attempt to place a queen in the given row of an NxN board
    taking into account the given positions of other queens.
    Recursively attempt to place a queen in the next row
    and backtrack when necessary.
    Returns true upon success.
    """
    for col in range(n):
        position = (row, col)
        if is_safe(position, queens):
            queens.append(position) # tentatively place queen
            if row+1 < n:
                if solve_recursively(n, row+1, queens):
                    return True
                else:
                    del queens[-1] # backtrack
            else:
                return True
    return False


def solve(n):
    """
    Attempt to place N queens on an NxN board.
    Returns a list of N positions upon success.
    Returns an empty list upon failure.
    """
    row = 0
    queens = list()
    solve_recursively(n, row, queens)
    return queens


def test():
    for n in range(1, 9):
        queens = solve(n)
        print('placed', len(queens), 'queens on', n, 'x', n, 'board')
        print(queens)

test()
