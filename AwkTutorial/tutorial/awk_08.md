# Two files processing

This section focuses on solving problems which depend upon the contents of two or more files. These are usually based on comparing records and fields. These two files will be used in the examples to follow:

```bash
$ paste c1.txt c2.txt
Blue    Black
Brown   Blue
Orange  Green
Purple  Orange
Red     Pink
Teal    Red
White   White
```

Suppose, you want to find common lines between two files. The *key* features used in the solution below:

* For two files as input, `NR==FNR` will be *true* only when the first file is being processed
* `next` will skip the rest of the code and fetch the next record
* `a[$0]` by itself is a valid statement, creates an uninitialized element in array `a` with `$0` as the key (if the key doesn't exist yet)
* `$0 in a` checks if the given string (`$0` here) exists as a key in the array `a`

```bash
# common lines, same as: grep -Fxf c1.txt c2.txt
$ awk 'NR==FNR{a[$0]; next} $0 in a' c1.txt c2.txt
Blue
Orange
Red
White

# lines present in c2.txt but not in c1.txt
$ awk 'NR==FNR{a[$0]; next} !($0 in a)' c1.txt c2.txt
Black
Green
Pink
```

> **Warning**: The `NR==FNR` logic will fail if the first file is empty, since `NR` wouldn't get a chance to increment. You can set a flag after the first file has been processed to avoid this issue.

```bash
# no output
$ awk 'NR==FNR{a[$0]; next} !($0 in a)' /dev/null greeting.txt

# gives the expected output
$ awk '!f{a[$0]; next} !($0 in a)' /dev/null f=1 greeting.txt
Hi there
Have a nice day
Good bye
```

Here's an example for field based comparisons. The problem statement is to fetch all records from `marks.txt` if the first field matches any of the departments listed in the `dept.txt` file and the third field value is greater than `70`.

```bash
$ cat marks.txt
Dept    Name    Marks
ECE     Raj     53
ECE     Joel    72
EEE     Moi     68
CSE     Surya   81
EEE     Tia     59
ECE     Om      92
CSE     Amy     67

$ cat dept.txt
CSE
ECE

# note that dept.txt is used to build the array keys first
# use FNR==1 || ($1 in a && $3>70) if the header is needed as well
$ awk 'NR==FNR{a[$1]; next} $1 in a && $3>70' dept.txt marks.txt
ECE     Joel    72
CSE     Surya   81
ECE     Om      92
```

For multiple field comparison, you can use a `,` character between the fields — for example, `a[$1,$2]`. This will insert the value of the `SUBSEP` variable between the fields (non-printing character `\034` is the default value).
