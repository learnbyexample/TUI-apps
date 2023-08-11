### Questions

There are more than 100 exercises covering both the builtin `re` and third-party `regex` module. The initial questions cover the very basics of using `re` module functions. After that, you'll be required to use more and more regular expression features, roughly in the following order:

* Anchors
* Alternation and Grouping
* Escaping metacharacters
* Dot metacharacter and Quantifiers
* Working with matched portions
* Character class
* Groupings and backreferences
* Lookarounds
* regex module

There are two types of exercises:

* search related functions like `search()`, `fullmatch()`, etc
* other functions like `sub()`, `split()`, `findall()`, `finditer()`, etc

### Solution Input box

You can type the solution in the input box and press the **Enter** key to execute. For example, `re.search(r'cat', ip)` to check if `cat` is present in the input strings. `ip` is the variable that'll have the sample input (string or list of strings) for all the exercises.

The input box will accept a single valid Python expression. Some of the exercises will require you to use list comprehensions.

Some of the error types are caught. In such cases, the background color of the input box will change to *red* and the error message will be displayed below the box. Other errors might result in the app crashing.

The input box will turn *green* if the entered code solves all the sample input strings. A reference solution box will appear below the table in such cases. You can press **Ctrl+s** to show the solution box whenever you want.

For search related functions, the table below the input box will have a set of strings that should match and another set of strings that *shouldn't* match. These strings will be individually highlighted in *green* if the condition is satisfied and *red* otherwise.

For some exercises, you might need to view the representation of sample strings instead of how they are displayed on the screen. For example, to spot characters like tabs, newlines, backspaces, etc. You can switch between these views using the **str** and **repr** radio buttons. Lists and dicts won't be affected by this option. You can also use the **Ctrl+r** shortcut to toggle these radio buttons.

For other functions, the left column of the table will have a set of input with corresponding output in the right column. Each row will be highlighted in *green* or *red* based on the entered code satisfying the condition or not. You can switch between **expected** and **actual** radio buttons to view the expected and actual output in the right column. When you choose the **actual** option, the strings will be highlighted in *orange* if the output doesn't match the expected result. You can also use the **Ctrl+b** shortcut to toggle these radio buttons.

Use appropriate anchors based on whether the term **string** or **line** is used in the question description.

> **Warning:** There is no safeguard against the commands you have typed. They are treated as if you executed them from a Python program.

### Shortcuts

You can either click the buttons using mouse or press the key combinations listed below:

* **F1** view this guide
* **F2** view exercises
* **Ctrl+n** go to the next question
* **Ctrl+p** go to the previous question
* **Ctrl+s** show solution box
* **Ctrl+r** toggle between **str** and **repr**
* **Ctrl+b** toggle between **expected** and **actual**
* **Ctrl+t** toggle the theme between **light** and **dark** modes
* **Ctrl+c** or **Ctrl+q** quit the application

Shortcuts for navigating and editing in the solution box are listed below:

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

### User progress

Solutions you have typed are automatically saved in `user_progress.json` in the same directory as the script. This happens only when you press **Enter** to execute — navigating to another question and closing the app won't trigger the save logic.

Radio button and theme choices are also saved.

If you close the application and open it again, the first unsolved question will be displayed (i.e. already solved questions are skipped).

If you use **Ctrl+s**, the solution *won't* be saved — you'll have to type and execute the code to be considered for saving the changes.

Once you have solved a question, only a different correct solution can override the previously saved code.

### Understanding Python re(gex)?

The exercise questions in this app have been adapted from my ebook: [https://github.com/learnbyexample/py_regular_expressions](https://github.com/learnbyexample/py_regular_expressions)

