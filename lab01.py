#!/usr/bin/env python3

def reciprocal_sum(limit, bias=0):
    """Compute the sum of reciprocals from 1..limit.

    An optional bias is applied before (and removed after)
    computing the sum in order to demonstrate the limited
    precision of real numbers.
    """
    return bias + sum(1/n for n in range(1, limit + 1)) - bias


print('Bias 0:', reciprocal_sum(1000))
print('Bias 1e12:', reciprocal_sum(1000, bias=1e12))
