### Regex Playground

You can type the search pattern in the **Compile** input box and press the **Enter** key (or **Ctrl+r**) to execute. For example, `re.compile(r'\d')` to match digit characters. Matching portions will be highlighted in red.

The compiled pattern is available via the `pat` variable and you can use `ip` to refer to the input string. You can transform or extract data by typing appropriate expression in the **Action** box. For example, `pat.sub(r'(\g<0>)', ip)` will add parenthesis around the matching portions.

You can skip the Compile box and directly use the Action box too. For example, `[m.span() for m in re.finditer(r'\d+', ip)]` to get the location of all the matching portions.

> **Warning:** There is no safeguard against the commands you have typed. They are treated as if you executed them from a Python program.

Press **F2** to get back to the Playground from other screens. You can also click the buttons at the top to navigate between the different screens.

### Changing ip

You can press **Ctrl+p** to edit the contents of the input string.

After making the changes, press **Ctrl+r** or navigate to Compile/Action box and press the **Enter** key to update the results for the changed data.

The input string is obtained from the `ip.txt` file located in the app directory. So, changing this file before starting the app is another option.

### Handling errors

Some of the error types are caught. In such cases, the background color of the input boxes will change to red and the error message will be displayed below the corresponding box. Other errors might result in the app crashing.

### Input box shortcuts

* Use the mouse to position the cursor anywhere you like
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
* **Enter** or **Ctrl+r** submit the code for execution

To navigate between widgets in the same screen:

* **Tab** to move to the next box
* **Shift+Tab** to move to the previous box

### Theme

Press **Ctrl+t** to toggle between light and dark themes.

### App Guide

Press **F1** to display this help screen.

### Cheatsheet

Press **F3** to display a cheatsheet for Python regular expressions.

### Interactive Examples

Press **F4** for regular expression examples covering various topics. You can modify the code snippets and pressing the **Enter** key will update the corresponding output. Press **Ctrl+z** to discard changes and reload the examples.

> **Warning:** There is no safeguard against the commands you have typed. They are treated as if you executed them from a Python program.

