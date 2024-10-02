def sort_by_value(d):
    return {k:d[k] for k in sorted(d, key=lambda k: d[k])}

marks = dict(Rahul=86, Ravi=92, Rohit=75, Rajan=79, Ram=95)
assert sort_by_value(marks) == {'Rohit': 75, 'Rajan': 79, 'Rahul': 86, 'Ravi': 92, 'Ram': 95}
assert sort_by_value({}) == {}
assert sort_by_value({1: 'banana', 2: 'apple'}) == {2: 'apple', 1: 'banana'}

print('all tests passed')
