# Default field separation

`awk` automatically splits input into fields based on one or more sequence of **space** or **tab** or **newline** characters. In addition, any of these three characters at the start or end of input gets trimmed and won't be part of field contents. The fields are accessible using `$N` where `N` is the field number you need. You can also pass an expression instead of numeric literals to specify the field required.

Here are some examples:

```bash
$ cat table.txt
brown bread mat hair 42
blue cake mug shirt -7
yellow banana window shoes 3.14

# print the second field of each input line
$ awk '{print $2}' table.txt
bread
cake
banana

# print lines only if the last field is a negative number
$ awk '$NF<0' table.txt
blue cake mug shirt -7

# print the field as specified by the value stored in the 'f' variable
# -v option helps you set a value for the given variable
$ awk -v f=3 '{print $f}' table.txt
mat
mug
window
```

Here's an example of applying a substitution operation for a particular field.

```bash
# delete lowercase vowels only from the first field
# gsub() is like the sed substitution command with the 'g' flag
# use sub() if you need to change only the first match
# 1 is a true condition, and thus prints the contents of $0
$ awk '{gsub(/[aeiou]/, "", $1)} 1' table.txt
brwn bread mat hair 42
bl cake mug shirt -7
yllw banana window shoes 3.14
```
