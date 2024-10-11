def sum_file_nums(ip_file, floating=False):
    total = 0
    str2num = int
    if floating:
        str2num = float
    with open(ip_file) as f:
        for line in f:
            for w in line.split():
                try:
                    total += str2num(w)
                except ValueError:
                    pass
    return total

filename = 'sample_files/n1.txt'

# only integers
expected_op = -335
assert sum_file_nums(filename) == expected_op

# both integers and floating-point numbers
expected_op = -3463.2599999999998
from math import isclose
assert isclose(sum_file_nums(filename, floating=True), expected_op)

print('all tests passed')
