#!/usr/bin/env python3

def f(x):
    if x > 100:
        return x - 10
    else:
        return g(f(x + 11))
    
def g(x):
    if x > 100:
        return x - 10
    else:
        return f(g(x + 11))

def test():
    for x in range(200):
        print('f(' + str(x) + ') =', f(x))

# test()

print('on what input would you like me to run the function')
arg = input()
print('f(' + arg + ') =', f(int(arg)))
