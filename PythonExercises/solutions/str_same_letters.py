def str_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

assert str_anagram('god', 'Dog')
assert str_anagram('beat', 'abet')
assert str_anagram('Tap', 'paT')
assert not str_anagram('beat', 'table')
assert not str_anagram('seat', 'teal')

print('all tests passed')
