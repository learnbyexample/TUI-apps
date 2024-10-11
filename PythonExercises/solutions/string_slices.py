def slice(s):
    c = len(s)
    if c < 3:
        return [s]
    return [s[i:j+1] for i in range(c) for j in range(i+1, c)]

assert slice('') == ['']
assert slice('a') == ['a']
assert slice('to') == ['to']
assert slice('cat') == ['ca', 'cat', 'at']
assert slice('kite') == ['ki', 'kit', 'kite', 'it', 'ite', 'te']
assert slice('table') == ['ta', 'tab', 'tabl', 'table', 'ab', 'abl', 'able', 'bl', 'ble', 'le']

print('all tests passed')
