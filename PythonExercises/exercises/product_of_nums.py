def product(iterable):
    # add your solution here

from math import isclose
assert isclose(product([-4, 2.3e12, 77.23, 982, 0b101]), -3.48863356e+18)
assert product(range(2, 6)) == 120
assert product({42, 5, 1, -2, 3, -7}) == 8820

try:
    product(())
except TypeError as e:
    assert str(e) == 'at least one number expected'

try:
    product([[1, 2], 3])
except TypeError as e:
    assert str(e) == 'int or float expected'

try:
    product(['a', 'b'])
except TypeError as e:
    assert str(e) == 'int or float expected'

print('all tests passed')
