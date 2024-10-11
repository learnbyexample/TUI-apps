def slice(s):
    # add your solution here

assert slice('') == ['']
assert slice('a') == ['a']
assert slice('to') == ['to']
assert slice('cat') == ['ca', 'cat', 'at']
assert slice('kite') == ['ki', 'kit', 'kite', 'it', 'ite', 'te']
assert slice('table') == ['ta', 'tab', 'tabl', 'table', 'ab', 'abl', 'able', 'bl', 'ble', 'le']

print('all tests passed')
