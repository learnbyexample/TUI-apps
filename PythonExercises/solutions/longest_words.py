def longest(ip_file):
    with open(ip_file) as f:
        sorted_words = sorted(f.read().split(), key=len, reverse=True)
    op = set()
    if sorted_words:
        first = sorted_words[0]
        word_size = len(first)
        op.add(first)
    for w in sorted_words[1:]:
        if len(w) == word_size:
            op.add(w)
        else:
            break
    return op

filename = 'sample_files/f1.txt'
expected_op = {'rhinestone', 'PERISHABLE', 'invaluable'}
longest(filename) == expected_op

filename = 'sample_files/f2.txt'
expected_op = {'beginning', 'REwoRkinG'}
longest(filename) == expected_op

filename = 'sample_files/f3.txt'
expected_op = set()
longest(filename) == expected_op

print('all tests passed')
