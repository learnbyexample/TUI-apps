def add_time(t1, t2):
    h1, m1, s1 = t1.split(':')
    h2, m2, s2 = t2.split(':')
    c, s3 = divmod(int(s1) + int(s2), 60)
    c, m3 = divmod(c + int(m1) + int(m2), 60)
    d, h3 = divmod(c + int(h1) + int(h2), 24)
    return f'{d:02}-{h3:02}:{m3:02}:{s3:02}'

assert add_time('01:02:03', '4:5:6') == '00-05:07:09'
assert add_time('63:98:24', '84:2:76') == '06-04:41:40'
assert add_time('99:99:99', '99:99:99') == '08-09:21:18'
assert add_time('0:52:33', '0:6:27') == '00-00:59:00'

print('all tests passed')
