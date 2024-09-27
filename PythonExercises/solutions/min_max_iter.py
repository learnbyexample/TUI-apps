def min_max(iterable):
    first = True
    for n in iterable:
        if first:
            minimum = maximum = n
            first = False
            continue
        if n > maximum:
            maximum = n
        if n < minimum:
            minimum = n
    return minimum, maximum

assert min_max('visualization') == ('a', 'z')
assert min_max({10, -42, 53.2, -3}) == (-42, 53.2)
assert min_max([0]) == (0, 0)
assert min_max({'Raj': 86, 'Zak': 92, 'Joe': 75, 'Amy': 79}) == ('Amy', 'Zak')
assert min_max(range(-2, 20, 4)) == (-2, 18)

print('all tests passed')
