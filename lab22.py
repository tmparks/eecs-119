#!/usr/bin/env python3

def integral(x):
    """
    Approximate an integral by summing the terms of a series.
    The argument must be in the interval (0,1]
    """
    if not (0 < x and x <= 1):
        raise ValueError('argument must be in the interval (0,1]')
    sum = x
    numerator = x
    factorial = 1
    small_enough = 1e-6
    limit = 15
    reason = 'Aborted'
    for n in range(1, limit):
        denominator = factorial * (2 * n + 1)
        term = numerator / denominator
        sum += term
        numerator *= -x * x
        factorial *= n
        if abs(term) < small_enough:
            reason = 'Accurate'
            break
    return (sum, abs(term), '{} after {} iterations'.format(reason, n + 1))


# x = 0.352234607
x = 0.587040260
(sum, error, reason) = integral(x)
print('integral({}) = {} +/- {}'.format(x, sum, error))
print(reason)
