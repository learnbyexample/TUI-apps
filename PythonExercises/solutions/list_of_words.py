import re

def extract_words(s):
    return re.findall(r'[a-zA-Z]+', s)

assert extract_words(' apple banana_cherry  ') == ['apple', 'banana', 'cherry']
s = '"Hi", there! How *are* you? All fine here.'
assert extract_words(s) == ['Hi', 'there', 'How', 'are', 'you', 'All', 'fine', 'here']
s = 'This-Is-A:Colon:Separated,Phrase'
assert extract_words(s) == ['This', 'Is', 'A', 'Colon', 'Separated', 'Phrase']
assert extract_words('αλεπού 42') == []

print('all tests passed')
