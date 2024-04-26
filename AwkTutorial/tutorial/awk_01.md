# Regexp filtering

`awk` provides filtering capabilities like those supported by the `grep` and `sed` commands, along with some more nifty features. And similar to many command line utilities, `awk` can accept input from both `stdin` and files.

By default, `awk` automatically loops over the input content line by line. You can then use programming instructions to process those lines. Here are some basic examples:

```bash
# same as: grep 'at' and sed -n '/at/p'
$ printf 'gate\napple\nwhat\nkite\n' | awk '/at/'
gate
what

# same as: grep -v 'e' and sed -n '/e/!p'
$ printf 'gate\napple\nwhat\nkite\n' | awk '!/e/'
what

# lines containing 'e' followed by zero or more characters and then 'y'
$ awk '/e.*y/' greeting.txt
Have a nice day
```

In the above examples, only the filtering condition was given. By default, when the condition evaluates to `true`, the contents of `$0` (input record) is printed. Thus:

* `awk '/regexp/'` is a shortcut for `awk '$0 ~ /regexp/{print $0}'`
* `awk '!/regexp/'` is a shortcut for `awk '$0 !~ /regexp/{print $0}'`
