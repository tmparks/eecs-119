#!/usr/bin/env python3

n = list() # initially empty

def swap(left, right):
    """
    Swap two elements and move the left and right indices
    """
    temp = n[left]
    n[left] = n[right]
    n[right] = temp
    left += 1
    right -= 1
    return (left, right)

def quicksort(i, j):
    left = i+1
    right = j
    pick = n[i]
    while left <= right:
        while n[left] < pick: # go left until an element is out of place
            left += 1
        while n[right] > pick: # go right until an element is out of place
            right -= 1
        if left <= right: # interchange the elements
            (left, right) = swap(left, right)
    if right > i: # recurse on smaller problems
        quicksort(i, right)
    if left < j:
        quicksort(left, j)

size = 15 # maximum problem size
print('I can sort arrays of size up to', size)
arraysize = int(input('How large an array would you like to sort? '))
print('Now enter the elements of your array, each on a separate line')
for k in range(arraysize):
    n.append(int(input()))
quicksort(1, arraysize)
print('Sorted numbers are ')
for k in range(arraysize):
    print(n[k])
