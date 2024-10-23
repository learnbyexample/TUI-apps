def alphabetic_word(word):
    # add your solution here

def alphabetic_sentence(sentence):
    # add your solution here

# ascending order
assert alphabetic_word('AborT')
assert alphabetic_word('access')
assert alphabetic_word('adopt')
assert alphabetic_word('blot')
assert alphabetic_word('cells')
# descending order
assert alphabetic_word('Rome')
assert alphabetic_word('spooned')
assert alphabetic_word('yuppie')
assert alphabetic_word('zoomed')

assert not alphabetic_word('are')
assert not alphabetic_word('boat')
assert not alphabetic_word('Flee')

# sentence checks
assert alphabetic_sentence('Toe got bit')
assert alphabetic_sentence('Miffed to be almost spooked')
assert not alphabetic_sentence('All is well')

print('all tests passed')
