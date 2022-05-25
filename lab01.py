#!/usr/bin/env python3

def reciprocal_sum(limit, bias=0):
    sum = bias
    for n in range(1, limit + 1):
        sum += 1/n
    sum -= bias
    return sum

print("Bias 0: {}".format(reciprocal_sum(1000)))
print("Bias 1e12: {}".format(reciprocal_sum(1000, bias=1e12)))
