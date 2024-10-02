def remove_duplicates(seq):
    return list(dict.fromkeys(seq))

nums = [1, 4, 6, 22, 3, 5, 4, 3, 6, 2, 1, 51, 3, 1]
assert remove_duplicates(nums) == [1, 4, 6, 22, 3, 5, 2, 51]
assert remove_duplicates('abracadabra') == ['a', 'b', 'r', 'c', 'd']

print('all tests passed')
