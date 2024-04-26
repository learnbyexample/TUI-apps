# Interactive awk tutorial

Hello! This interactive tutorial aims to give a brief tour of the `GNU awk` command. `awk` is a programming language and widely used for text processing tasks from the command line.

### Table of Contents

1) Interactive awk tutorial
2) Regexp filtering
3) Special variables
4) Default field separation
5) Condition and Action
6) Regexp field processing
7) Record separators
8) State machines
9) Two files processing
10) Removing duplicates
11) Further Reading

### App Guide

Example commands in this tutorial are interactive! Which means you can modify them and press the **Enter** key to execute. Go on, try out a few commands you know with the sample shown below:

```bash
# same as: cat greeting.txt
$ awk '1' greeting.txt
Hi there
Have a nice day
Good bye
```

`/bin/sh` is the shell interpreting the commands (`subprocess` module's default setting). So, features like brace expansion and process substitution won't work.

> **Warning:** There is no safeguard against the commands you have typed. They are treated as if you executed them from a shell session. For example, you can use `ls` and `tree` commands to browse the contents of the current directory.

You can either click the buttons using mouse or press the key combinations listed below:

* **Ctrl+n** go to the next section
* **Ctrl+p** go to the previous section
* **Ctrl+r** reset the current tutorial section (changes made are discarded)
* **Ctrl+t** toggle the theme between **light** and **dark** modes
* **Ctrl+c** or **Ctrl+q** quit the application

Shortcuts for navigating and editing in the input command box are listed below:

* Use mouse click to position the cursor in any of the command boxes
* **Tab** move to the next command box
* **Shift+Tab** move to the previous command box
* **←** move left by one character
* **→** move right by one character
* **Home** or **Ctrl+a** move to the start of the line
* **End** or **Ctrl+e** move to the end of the line
* **Ctrl+←** move to the start of the current/previous word
* **Ctrl+→** move to the start of the next word
* **Ctrl+w** delete till the start of the current/previous word
* **Ctrl+f** delete till the start of the next word
* **Ctrl+u** delete till the start of the line
* **Ctrl+k** delete till the end of the line
* **Backspace** or **Ctrl+h** delete character to the left of the cursor
* **Delete** or **Ctrl+d** delete character under the cursor
* **Enter** submit the command for execution
