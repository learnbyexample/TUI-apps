# Record separators

By default, newline is used as the input and output record separators. Here are some examples of changing the input record separator by assigning the `RS` variable:

```bash
# change the input record separator to a comma character
# note the content of the 2nd record where newline is just another character
$ printf 'this,is\na,sample,text' | awk -v RS=, '{print NR ")", $0}'
1) this
2) is
a
3) sample
4) text

# print records containing 'i' as well as 't'
$ printf 'Sample123string42with777numbers' | awk -v RS='[0-9]+' '/i/ && /t/'
string
with
```

Here's an example of changing the output record separator:

```bash
$ seq 9 | awk '{ORS = NR%3 ? "-" : "\n"} 1'
1-2-3
4-5-6
7-8-9
```

As a special case, when `RS` is set to an empty string, one or more consecutive empty lines is used as the input record separator.

```bash
$ printf 'apple\nbanana\nfig\n\n\n123\n456' | awk -v RS= 'NR==1'
apple
banana
fig
```
