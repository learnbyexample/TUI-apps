def palindrome(start=1, stop=10000):
    op = []
    for n in range(start, stop+1):
        dec_s = str(n)
        bin_s = f'{n:b}'
        if dec_s == dec_s[::-1] and bin_s == bin_s[::-1]:
            op.append(n)
    return op

expected_op = [1, 3, 5, 7, 9, 33, 99, 313, 585, 717, 7447, 9009]
assert palindrome() == expected_op
assert palindrome(42564, 73737) == [53235, 53835, 73737]

print('all tests passed')
