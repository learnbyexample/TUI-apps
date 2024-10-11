def sum_file_nums(ip_file, floating=False):
    # add your solution here

filename = 'sample_files/n1.txt'

# only integers
expected_op = -335
assert sum_file_nums(filename) == expected_op

# both integers and floating-point numbers
expected_op = -3463.2599999999998
from math import isclose
assert isclose(sum_file_nums(filename, floating=True), expected_op)

print('all tests passed')
