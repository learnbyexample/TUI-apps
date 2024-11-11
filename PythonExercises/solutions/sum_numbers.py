def sum_nums(*args, initial=0):
    total = initial
    for n in args:
        total += n
    return total

assert sum_nums() == 0
assert sum_nums(3, -8) == -5
assert sum_nums(1, 2, 3, 4, 5, initial=5) == 20
from math import isclose
assert isclose(sum_nums(3.14, -341.5234e-6, 42, 4e2, 7.89), 453.0296584766)

print('all tests passed')
