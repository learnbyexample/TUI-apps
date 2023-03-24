# Python Regular Expressions Cheatsheet

From [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html):

>A regular expression (or RE) specifies a set of strings that matches it; the functions in this module let you check if a particular string matches a given regular expression

An overview of regular expression syntax as implemented by the `re` built-in module is shown below. Assume ASCII character set unless otherwise specified.
 
The cheatsheet and examples presented in this app are based on the contents of my **Understanding Python re(gex)?** ebook. Visit my GitHub repo [https://github.com/learnbyexample/py_regular_expressions](https://github.com/learnbyexample/py_regular_expressions) for details.

### Anchors

| Anchors | Description |
| ------------- | ----------- |
| `\A` | restricts the match to the start of string |
| `\Z` | restricts the match to the end of string |
| `^` | restricts the match to the start of line |
| `$` | restricts the match to the end of line |
| `\n` | newline character is used as line separator |
| `re.MULTILINE` or `re.M` | flag to treat input as multiline string |
| `\b` | restricts the match to the start/end of words |
|  | word characters: alphabets, digits, underscore |
| `\B` | matches wherever `\b` doesn't match |

`^`, `$` and `\` are metacharacters in the above table, as these characters have special meaning. Prefix a `\` character to remove the special meaning and match such characters literally. For example, `\^` will match a `^` character instead of acting as an anchor.

### Alternation and Grouping

| Feature | Description |
| ------------- | ----------- |
| `\|` | multiple RE combined as conditional OR |
|   | each alternative can have independent anchors  |
| `(pat)` | group pattern(s), also a capturing group |
| | `a(b\|c)d` is same as `abd\|acd` |
| `(?:pat)` | non-capturing group |
| `(?P<name>pat)` | named capture group |

### Quantifiers

| Quantifiers | Description |
| ------------- | ----------- |
| `*` | Match zero or more times |
| `+` | Match one or more times |
| `?` | Match zero or one times |
| `{m,n}` | Match `m` to `n` times (inclusive) |
| `{m,}` | Match at least `m` times |
| `{,n}` | Match up to `n` times (including `0` times) |
| `{n}` | Match exactly `n` times |
| `pat1.*pat2` | any number of characters between `pat1` and `pat2` |
| `pat1.*pat2\|pat2.*pat1` | match both `pat1` and `pat2` in any order |

The above table is for greedy quantifiers. Greedy here means that these quantifiers will match as much as possible that'll also honor the overall RE. Appending a `?` to greedy quantifiers makes them **non-greedy**, i.e. match as *minimally* as possible. Appending a `+` to greedy quantifiers makes them **possessive**, which prevents backtracking. You can also use `(?>pat)` *atomic grouping* to safeguard from backtracking. Quantifiers can be applied to literal characters, groups, backreferences and character classes.

### Dot metacharacter and Character class

| Class | Description |
| ------------- | ----------- |
| `.` | Match any character except the newline character `\n` |
| `[]` | Character class, matches one character among many |
| `[aeiou]` | Match any vowel |
| `[^aeiou]` | `^` inverts selection, so this matches any consonant |
| `[a-f]` | `-` defines a range, so this matches any of abcdef characters |
| `\d` | Match a digit, same as `[0-9]` |
| `\D` | Match non-digit, same as `[^0-9]` or `[^\d]` |
| `\w` | Match word character, same as `[a-zA-Z0-9_]` |
| `\W` | Match non-word character, same as `[^a-zA-Z0-9_]` or `[^\w]` |
| `\s` | Match whitespace character, same as `[\ \t\n\r\f\v]` |
| `\S` | Match non-whitespace character, same as `[^\ \t\n\r\f\v]` or `[^\s]` |

### Lookarounds

| Lookarounds | Description |
| ------- | ----------- |
| lookarounds | custom assertions, zero-width like anchors |
| `(?!pat)` | negative lookahead assertion |
| `(?<!pat)` | negative lookbehind assertion |
| `(?=pat)` | positive lookahead assertion |
| `(?<=pat)` | positive lookbehind assertion |
| `(?!pat1)(?=pat2)` | multiple assertions can be specified in any order |
|  | as they mark a matching location without consuming characters |
| `((?!pat).)*` | Negate a grouping, similar to negated character class |

### Flags

| Flags | Description |
| ------------- | ----------- |
| `re.IGNORECASE` or `re.I` | flag to ignore case |
| `re.DOTALL` or `re.S` | allow `.` metacharacter to match newline character |
| `flags=re.S\|re.I` | multiple flags can be combined using `\|` operator |
| `re.MULTILINE` or `re.M` | allow `^` and `$` anchors to match line wise |
| `re.VERBOSE` or `re.X` | allows to use literal whitespaces for aligning purposes |
|  | and to add comments after the `#` character |
|  | escape spaces and `#` if needed as part of actual RE |
| `re.ASCII` or `re.A` | match only ASCII characters for `\b`, `\w`, `\d`, `\s` |
|  | and their opposites, applicable only for Unicode patterns |
| `re.LOCALE` or `re.L` | use locale settings for byte patterns and 8-bit locales |
| `(?#comment)` | another way to add comments, not a flag |
| `(?flags:pat)` | inline flags only for this `pat`, overrides `flags` argument |
|  | flags is `i` for `re.I`, `s` for `re.S`, etc, except `L` for `re.L` |
| `(?-flags:pat)` | negate flags only for this `pat` |
| `(?flags-flags:pat)` | apply and negate particular flags only for this `pat` |
| `(?flags)` | apply flags for whole RE, can be used only at start of RE |
|  |  anchors if any, should be specified after `(?flags)` |

### Working with matched portions

| Matched portion | Description |
| ------------- | ----------- |
| `re.Match` object | details like matched portions, location, etc |
| `m[0]` or `m.group(0)` | entire matched portion of `re.Match` object `m` |
| `m[n]` or `m.group(n)` | matched portion of *n*th capture group |
| `m.groups()` | tuple of all the capture groups' matched portions |
| `m.span()` | start and end+1 index of entire matched portion |
| | pass a number to get span of that particular capture group |
| | can also use `m.start()` and `m.end()` |
| `\N` | backreference, gives matched portion of *N*th capture group |
|  | applies to both search and replacement sections |
|  | possible values: `\1`, `\2` up to `\99` provided no more digits |
| `\g<N>` | backreference, gives matched portion of Nth capture group |
|  | possible values: `\g<0>`, `\g<1>`, etc (not limited to 99) |
|  | `\g<0>` refers to the entire matched portion |
| `(?P<name>pat)` | named capture group |
|  | refer as `'name'` in `re.Match` object |
|  | refer as `(?P=name)` in search section |
|  | refer as `\g<name>` in replacement section |
| `groupdict()` | method applied on a `re.Match` object |
|  | gives named capture group portions as a `dict` |

>**Note:** `\0` and `\100` onwards are considered as octal values, hence cannot be used as backreferences.

### re module functions

| Function | Description |
| ------------- | ----------- |
| `re.search` | Check if given pattern is present anywhere in input string |
|  | Output is a `re.Match` object, usable in conditional expressions |
|  | r-strings preferred to define RE |
|  | Use byte pattern for byte input |
|  | Python also maintains a small cache of recent RE |
| `re.fullmatch` | ensures pattern matches the entire input string |
| `re.compile` | Compile a pattern for reuse, outputs `re.Pattern` object |
| `re.sub` | search and replace |
| `re.sub(r'pat', f, s)` | function `f` with `re.Match` object as argument |
| `re.escape` | automatically escape all metacharacters |
| `re.split` | split a string based on RE |
| | text matched by the groups will be part of the output |
| | portion matched by pattern outside group won't be in output |
| `re.findall` | returns all the matches as a list |
| | if 1 capture group is used, only its matches are returned |
| | 1+, each element will be tuple of capture groups |
| | portion matched by pattern outside group won't be in output |
| `re.finditer` | iterator with `re.Match` object for each match |
| `re.subn` | gives tuple of modified string and number of substitutions |

The function definitions are given below:

```python
re.search(pattern, string, flags=0)
re.fullmatch(pattern, string, flags=0)
re.compile(pattern, flags=0)
re.sub(pattern, repl, string, count=0, flags=0)
re.escape(pattern)
re.split(pattern, string, maxsplit=0, flags=0)
re.findall(pattern, string, flags=0)
re.finditer(pattern, string, flags=0)
re.subn(pattern, repl, string, count=0, flags=0)
```

