### Exercises

There are more than 80 exercises intended to be solved using `GNU awk`. Some exercises will require you to combine `awk` with other CLI tools such as `tac`.

These problems have been adapted from my [CLI text processing with GNU awk](https://github.com/learnbyexample/learn_gnuawk) ebook. The chapters covered in this app are roughly in the following order:

* awk introduction
* Regular Expressions
* Field separators
* Record separators
* Control Structures
* Built-in functions
* Multiple file input
* Processing multiple records
* Two file processing
* Dealing with duplicates

### Input command box

You can type the command in the input box and press the **Enter** key to execute. For example, `awk -F, '{print $1}' scores.csv` to display the first field from the `scores.csv` file.

`/bin/sh` is the shell interpreting the commands (`subprocess` module's default setting). So, features like brace expansion and process substitution won't work.

> **Warning:** There is no safeguard against the commands you have typed. They are treated as if you executed them from a shell session. For example, you can use `ls` and `tree` commands to browse the contents of the current directory.

### Output and reference solutions

Output (`stdout`) of the command is displayed below the input box. If the output matches the expected result, the input box will turn *green* and a reference solution box will also appear.

If the exit status of the command executed is non-zero, the output box will turn *red* and display text from the `stderr` stream. There is also a **two** second timeout for commands taking too long. For example, commands like `cat` and `grep` will wait forever for `stdin` data if you forget to provide an input source.

### Input files

Content of the input files and expected output for each exercise are shown in boxes with appropriate labels. You might have to scroll (using mouse or the scrollbar) for longer files.

You can click the **Directory** tab at the top of the screen to browse the contents of the current working directory. Click on a particular file to view its contents.

### Shortcuts

You can either click the buttons using mouse or press the key combinations listed below:

* **F1** view this guide
* **F2** view exercises
* **F3** view directory
* **Ctrl+n** go to the next question
* **Ctrl+p** go to the previous question
* **Ctrl+s** toggle reference solution box
* **Ctrl+t** toggle the theme between **light** and **dark** modes
* **Ctrl+c** or **Ctrl+q** quit the application

Shortcuts for navigating and editing in the input command box are listed below:

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
* **Enter** submit the command for execution

### User progress

Commands you have typed are automatically saved in `user_progress.json` in the same directory as the script. This happens only when you press **Enter** to execute — navigating to another question and closing the app won't trigger the save logic.

Theme choice is also saved.

If you close the application and open it again, the first unsolved question will be displayed (i.e. already solved questions are skipped).

Using **Ctrl+s** *won't* trigger the save logic — you'll have to type and execute the command to be considered for saving the changes.

Once you have solved a question, only a different correct solution can override the previously saved command.

### CLI text processing with GNU awk

The exercise questions in this app have been adapted from my ebook: [https://github.com/learnbyexample/learn_gnuawk](https://github.com/learnbyexample/learn_gnuawk)

