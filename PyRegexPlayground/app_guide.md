# App Guide

### Playground

You can type the search pattern in the **Compile** input box and press the **Enter** key to execute. For example, `re.compile(r'\d')` to match digit characters. Matching portions will be highlighted in red.

The compiled pattern is available via the `pat` variable and you can use `ip` to refer to the input string. You can transform or extract data by typing appropriate expression in the **Action** box. For example, `pat.sub(r'(\g<0>)', ip)` will add parenthesis around the matching portions.

You can skip the Compile box and directly use the Action box too. For example, `[m.span() for m in re.finditer(r'\d+', ip)]` to get the location of all the matching portions.

> **Warning:** There is no safeguard against the commands you have typed. They are treated as if you executed them from a Python program.

### Changing ip

The input string is obtained from the `ip.txt` file. You can change contents of this file and press **Ctrl+p** to update the `ip` variable. You'll have to press **Enter** again to update the results for the changed data.

If you cloned the repo, you'd be able to easily spot the `ip.txt` file in the same directory as the script you are running. If you installed the app via the `pip` command in a virtual environment, you'll have to locate this file first. For example:

```bash
# go to the virtual environment
$ find -name pyregex_playground.py
./lib/python3.8/site-packages/regexplayground/pyregex_playground.py

$ find -name ip.txt
./lib/python3.8/site-packages/regexplayground/ip.txt
```

This convoluted procedure will be simplified in the future by adding a widget for accepting multiline user input.

### Handling errors

Some of the error types are caught. In such cases, the background color of the input boxes will change to red and the error message will be displayed below the corresponding box. Other errors might result in the app crashing.

### Input box shortcuts

* Use mouse click to position the cursor anywhere you like
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
* **Enter** submit the code for execution

When there are multiple input boxes in the same screen:

* **Tab** or **↓** to move to the next box
* **Shift+Tab** or **↑** to move to the previous box

### Theme

Press **Ctrl+t** to toggle the theme between light and dark modes.

### App Guide

Press **F1** to display this help text from the playground screen. Press **Ctrl+n** to toggle table of contents. Press **Esc** to go back.

### Cheatsheet

Press **F2** to display a cheatsheet for Python regular expressions. Press **Ctrl+n** to toggle table of contents. Press **Esc** to go back.

### Interactive Examples

Press **F3** for regular expression examples covering various topics. You can modify the code snippets and pressing the **Enter** key will update the corresponding output. Press **Ctrl+r** to discard changes and reload the examples. Press **Esc** to go back.

> **Warning:** There is no safeguard against the commands you have typed. They are treated as if you executed them from a Python program.

