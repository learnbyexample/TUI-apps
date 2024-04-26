# Condition and Action

The examples so far have used a few different ways to construct a typical `awk` one-liner. If you haven't yet grasped the syntax, this generic structure might help:

`awk 'cond1{action1} cond2{action2} ... condN{actionN}'`

If a condition isn't provided, the action is always executed. Within a block, you can provide multiple statements separated by a semicolon character. If action isn't provided, then by default, contents of `$0` variable is printed if the condition evaluates to *true*. Idiomatically, `1` is used to denote a `true` condition in one-liners as a shortcut to print the contents of `$0` (as seen in an earlier example). When action isn't present, you can use semicolon to terminate the condition and start another `condX{actionX}` snippet.

You can use a `BEGIN{}` block when you need to execute something before the input is read and an `END{}` block to execute something after all of the input has been processed.

```bash
$ seq 2 | awk 'BEGIN{print "---"} 1; END{print "%%%"}'
---
1
2
%%%
```
