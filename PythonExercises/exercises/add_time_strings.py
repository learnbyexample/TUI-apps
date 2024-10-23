def add_time(t1, t2):
    # add your solution here

assert add_time('01:02:03', '4:5:6') == '00-05:07:09'
assert add_time('63:98:24', '84:2:76') == '06-04:41:40'
assert add_time('99:99:99', '99:99:99') == '08-09:21:18'
assert add_time('0:52:33', '0:6:27') == '00-00:59:00'

print('all tests passed')
