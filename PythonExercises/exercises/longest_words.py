def longest(ip_file):
    # add your solution here

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
