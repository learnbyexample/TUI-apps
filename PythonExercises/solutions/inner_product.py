def sum_of_product(s1, s2):
    return sum(i * j for i, j in zip(s1, s2))

assert sum_of_product((1, 3, 5), [2, 4, 6]) == 44
assert sum_of_product([], []) == 0
from math import isclose
assert isclose(sum_of_product(range(3, 12, 2), [3.14, 0, -12, 6, 0.4223]), -15.9347)

print('all tests passed')
