def sqr_even_cube_odd(seq):
    return [n**3 if n%2 else n**2 for n in seq]

assert sqr_even_cube_odd([321, 1, -4, 0, 5, 2]) == [33076161, 1, 16, 0, 125, 4]
assert sqr_even_cube_odd((2, 4, 6)) == [4, 16, 36]

print('all tests passed')
