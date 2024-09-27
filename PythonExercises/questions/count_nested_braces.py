def max_nested_braces(expr):
    # add your solution here

assert max_nested_braces('a*b') == 0
assert max_nested_braces('a*b+{}') == 1
assert max_nested_braces('a*{b+c}') == 1
assert max_nested_braces('{a+2}*{b+c}') == 1
assert max_nested_braces('a*{b+c*{e*3.14}}') == 2
assert max_nested_braces('{{a+2}*{b+c}+e}') == 2
assert max_nested_braces('{{a+2}*{b+{c*d}}+e}') == 3
assert max_nested_braces('{{a+2}*{{b+{c*d}}+e*d}}') == 4
assert max_nested_braces('a*b{') == -1
assert max_nested_braces('a*{b+c}}') == -1
assert max_nested_braces('}a+b{') == -1
assert max_nested_braces('a*{b+c*{e*3.14}}}') == -1
assert max_nested_braces('{{a+2}*{{b}+{c*d}}+e*d}}') == -1

print('all tests passed')
