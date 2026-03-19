# Programming Assignment 6
## Problem 2

Backtracking is a technique which is used in various searching applications to
which computers are applied. The typical backtracking problem uses recursion in
two modes. In the first mode, it has a partial solution which it wants to extend
to a total solution. In the second mode, it has reached a dead end and wants to
partially back off from its solution in an attempt to find a working solution.

The problem we'd like you to solve with backtracking is that of placing N queens
on an NxN chess board in a configuration where no queen can capture any other
queen. For the uninitiated, a queen can capture any queen if there is a
vertical, horizontal or diagonal path connecting them.

In structruing a program to do this task, you want to write a function which
tests the validity of placing a queen in a new position given a current board.
This function will then be used in your backtracking program to differentiate
between valid and invalid situations.

Write and debug your program for the case where N=4. When it works, run some
other values of N until you discover values of N for which your program will not
generate a solution.
