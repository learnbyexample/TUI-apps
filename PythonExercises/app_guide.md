> **Warning:** This is a work-in-progress project.

### About

This interactive TUI app is intended to test the understanding of beginner to intermediate level Python learners.

### Script box

You can type the Python script in the TextArea widget and press **Ctrl+r** to execute it.

> **Warning:** There is no safeguard against the programs you execute. They are treated as if you executed them from a shell session.

### Output and reference solutions

Output of the script you execute is displayed below the TextArea widget. If the output matches the expected result, the script box will turn *green* and a reference solution box will also appear.

If the exit status of the program executed is non-zero, the output box will turn *red* and display text from the `stderr` stream. There is also a **five** second timeout to prevent cases like infinite loops from running forever.

### Directory

You can click the **Directory** tab at the top of the screen to browse the contents of the current working directory. Click on a particular file to view its contents.

### Shortcuts

You can either click the buttons using mouse or press the key combinations listed below:

* **F1** view this guide
* **F2** view exercises
* **F3** view directory
* **F4** change theme, quit the application and access command palette for the focused widget
* **Ctrl+r** execute the Python script
* **Ctrl+l** resets the script to the one provided initially for the exercise
    * previously saved script will be overwritten only after you press **Ctrl+r**
* **Ctrl+n** go to the next question
* **Ctrl+p** go to the previous question
* **Ctrl+s** toggle the reference solution box
* **Ctrl+t** toggle the theme between **light** and **dark** modes
* **Ctrl+c** or **Ctrl+q** quit the application

The **F4** key provides additional ways to toggle the theme and quit the app. You'll be able to view app level shortcuts as well as for the focused widget (which is the TextArea widget by default). Here are some selected shortcuts for editing and moving:

* **Home** or **Ctrl+a** move to the start of the line
* **End** or **Ctrl+e** move to the end of the line
* **Ctrl+←** move to the start of the current/previous word
* **Ctrl+→** move to the start of the next word
* **Ctrl+w** delete till the start of the word
* **Ctrl+f** delete till the end of the word
* **Ctrl+u** delete till the start of the line
* **Ctrl+k** delete till the end of the line
* **Ctrl+z** undo
* **Ctrl+y** redo

Some shortcuts were added in addition to the default options:

* **Ctrl+d** duplicate the current line
* **Ctrl+o** open a new line below with smart indentation

Pressing the **Tab** key adds 4 space characters (single indentation level). Pressing the **Enter** key will automatically add smart indentation based on contents of the current line. Similarly, the **Backspace** key will delete up to the previous indentation level.

### User progress

Scripts you have typed are automatically saved in `user_progress.json` in the app directory. This happens only when you press **Ctrl+r** to execute the script — navigating to another question and closing the app won't trigger the save logic.

Theme choice is also saved.

If you close the application and open it again, the first unsolved question will be displayed (i.e. already solved questions are skipped).

Using **Ctrl+s** *won't* trigger the save logic — you'll have to type and execute the script to be considered for saving the changes.

### 100 Page Python Intro

The exercise questions in this app have been adapted from my [100 Page Python Intro](https://github.com/learnbyexample/100_page_python_intro) ebook.

