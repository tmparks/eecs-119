#!/usr/bin/env python3
"""
Programming Assignment 6: Quicksort
"""


import random


def quicksort(n, i, j):
    """
    Recursively sort a list of numbers using the Quicksort algorithm
    """
    left = i
    right = j
    pick = n[i]
    while left <= right:
        while n[left] < pick:  # adjust left until an element is out of place
            left += 1
        while n[right] > pick:  # adjust right until an element is out of place
            right -= 1
        if left <= right:  # interchange the elements
            (n[left], n[right]) = (n[right], n[left])
            left += 1
            right -= 1
    if right > i:  # recurse on smaller problems
        quicksort(n, i, right)
    if left < j:
        quicksort(n, left, j)


def test():
    """
    Test cases.
    """
    for size in range(1, 30):
        numbers = []
        for _ in range(size):
            numbers.append(random.randrange(size))
        expected = sorted(numbers)
        result = numbers.copy()
        quicksort(result, 0, len(result) - 1)
        if result != expected:
            print('   input', numbers)
            print('  result', result)
            print('expected', expected)
    numbers = []
    print('Enter the elements of your array, all on one line')
    for word in input().split():
        numbers.append(int(word))
    quicksort(numbers, 0, len(numbers) - 1)
    print('Sorted numbers are ', numbers)


test()
