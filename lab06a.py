#!/usr/bin/env python3

def quicksort(n, i, j):
    left = i
    right = j
    pick = n[i]
    while left <= right:
        while n[left] < pick: # adjust left until an element is out of place
            left += 1
        while n[right] > pick: # adjust right until an element is out of place
            right -= 1
        if left <= right: # interchange the elements
            (n[left], n[right]) = (n[right], n[left])
            left += 1
            right -= 1
    if right > i: # recurse on smaller problems
        quicksort(n, i, right)
    if left < j:
        quicksort(n, left, j)

import random
def test():
    for size in range(1, 30):
        input = list()
        for _ in range(size):
            input.append(random.randrange(size))
        expected = sorted(input)
        result = input.copy()
        quicksort(result, 0, len(result) - 1)
        if result != expected:
            print('   input', input)
            print('  result', result)
            print('expected', expected)

test()

n = list()
print('Enter the elements of your array, all on one line')
for word in input().split():
    n.append(int(word))
quicksort(n, 0, len(n) - 1)
print('Sorted numbers are ', n)
