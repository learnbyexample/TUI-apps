def has_duplicates(iterable):
    # add your solution here

assert has_duplicates('pip') == True
assert has_duplicates(range(4)) == False
assert has_duplicates([3, 2, 3.0]) == True
assert has_duplicates({3.14, 5, 3, 3.14, 2, 1, 3}) == False
assert has_duplicates((('a', 2), 3, ('b',), ('a', 2))) == True

print('all tests passed')
