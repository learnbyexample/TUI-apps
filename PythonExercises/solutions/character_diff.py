def one_char_diff(w1, w2):
    if len(w1) != len(w2):
        return False

    w1, w2 = w1.lower(), w2.lower()
    for i in range(len(w1)):
        if w1[0:i] + w1[i+1:] == w2[0:i] + w2[i+1:]:
            return True
    return False

assert one_char_diff('A', 'b')
assert one_char_diff('A', 'a')
assert not one_char_diff('a', '')

assert one_char_diff('do', 'do')
assert one_char_diff('to', 'do')
assert one_char_diff('to', 'tz')
assert not one_char_diff('ab', '')
assert not one_char_diff('ab', 'be')

assert one_char_diff('par', 'car')
assert one_char_diff('par', 'Pat')
assert one_char_diff('par', 'par')
assert one_char_diff('par', 'paZ')
assert not one_char_diff('par', 'park')
assert not one_char_diff('par', 'Art')
assert not one_char_diff('par', 'pot')

assert one_char_diff('Food', 'good')
assert one_char_diff('food', 'fold')
assert one_char_diff('food', 'Food')
assert not one_char_diff('food', 'Foody')
assert not one_char_diff('food', 'fled')

print('all tests passed')
