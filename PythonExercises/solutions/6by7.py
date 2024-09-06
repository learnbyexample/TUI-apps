def six_by_seven(num):
    if num % 42 == 0:
        return 'Universe'
    elif num % 7 == 0:
        return 'Good'
    elif num % 6 == 0:
        return 'Food'
    else:
        return 'Oops'

assert six_by_seven(66) == 'Food'
assert six_by_seven(13) == 'Oops'
assert six_by_seven(42) == 'Universe'
assert six_by_seven(14) == 'Good'
assert six_by_seven(84) == 'Universe'
assert six_by_seven(235432) == 'Oops'

print('all tests passed')
