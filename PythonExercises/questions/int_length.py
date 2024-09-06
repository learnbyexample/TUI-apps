def len_int(n):
    # add your solution here

assert len_int(123) == 3
assert len_int(2) == 1
assert len_int(+42) == 2
assert len_int(-42) == 2
assert len_int(572342) == 6
assert len_int(962306349871524124750813401378124) == 33

try:
    len_int('a')
except TypeError as e:
    assert str(e) == 'provide only integer input'

print('all tests passed')
