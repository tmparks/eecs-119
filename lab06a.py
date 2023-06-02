#!/usr/bin/env python3

def quicksort(n, i, j):
    left = i+1
    right = j
    pick = n[i]
    while left <= right:
        while left <= j and n[left] <= pick: # adjust left until an element is out of place
            left += 1
        while right >= i and n[right] >= pick: # adjust right until an element is out of place
            right -= 1
        if left < right: # interchange the elements
            (n[left], n[right]) = (n[right], n[left])
            left += 1
            right -= 1
    if i < right: # move pick into position
        (n[i], n[right]) = (n[right], n[i])
        right -= 1
    if right > i: # recurse on smaller problems
        quicksort(n, i, right)
    if left < j:
        quicksort(n, left, j)

size = 15 # maximum problem size
n = list()
print('I can sort arrays of size up to', size)
arraysize = int(input('How large an array would you like to sort? '))
print('Now enter the elements of your array, each on a separate line')
for k in range(arraysize):
    n.append(int(input()))
quicksort(n, 0, arraysize-1)
print('Sorted numbers are ')
for k in range(arraysize):
    print(n[k])
