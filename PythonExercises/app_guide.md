### About

This interactive TUI app includes exercises and multiple-choice-questions intended to test the understanding of beginner to intermediate level Python learners.

### Script box

You can type the Python script in the TextArea widget. Pressing **Ctrl+r** will save the script to a local directory (`user_scripts`) and then execute it.

> **Warning:** There is no safeguard against the programs you execute. They are treated as if you executed them from a shell session.

### Output and reference solutions

Output of the script you execute is displayed below the TextArea widget. If the output matches the expected result, the script box will turn *green* and a reference solution box will also appear.

If the exit status of the program executed is non-zero, the output box will turn *red* and display text from the `stderr` stream. There is also a **two** second timeout to prevent cases like infinite loops from running forever.

### Quiz

Multiple choice questions are provided to check your understanding of Python concepts and features.

You can use the mouse to select a choice and then press the **Submit** button to check if the selected choice is correct or not.

Alternatively, you can use the **up**/**down** arrow keys followed by **Enter** to select a choice. Then, press **Ctrl+r** to submit the choice (you can also press **Tab** followed by **Enter**).

Once you have answered a quiz, you can no longer change your choice. The expected choice will be highlighted in *green*. The number of correctly answered questions will also be displayed.

### Directory

You can click the **Directory** tab at the top of the screen to browse the contents of the current working directory. Click on a particular file to view its contents.

### Shortcuts

You can either click the buttons using the mouse or press the key combinations listed below:

* **F1** view this guide
* **F2** view exercises
* **F3** view quiz
* **F4** view directory
* **F5** change theme, quit the application and access command palette for the focused widget
* **Ctrl+r** execute the Python script or submit the selected choice for quiz
* **Ctrl+l** resets the script to the one provided initially for the exercise
    * previously saved script will be overwritten only after you press **Ctrl+r**
* **Ctrl+n** go to the next question
* **Ctrl+p** go to the previous question
* **Ctrl+s** toggle the reference solution box
* **Ctrl+t** toggle the theme between **light** and **dark** modes
* **Ctrl+c** or **Ctrl+q** quit the application

The **F5** key provides additional ways to toggle the theme and quit the app. You'll be able to view app level shortcuts as well as for the focused widget. Some of the shortcuts for editing and moving are shown below:

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

Pressing the **Tab** key adds 4 space characters (single indentation level). Pressing the **Enter** key will automatically add smart indentation based on contents of the current line. Similarly, the **Backspace** key will delete up to the previous indentation level if the text before the cursor only has indented spaces.

### User progress

Scripts you have typed are automatically saved to a local directory (`user_scripts`). This happens only when you press **Ctrl+r** to execute the script — navigating to another question and closing the app won't trigger the save logic. The status for each attempted exercise is saved in the `exercise_progress.json` file. Theme choice is also saved.

Similarly, quiz progress is saved in the `quiz_progress.json` file.

If you close the application and open it again, the first unsolved question will be displayed (i.e. already solved questions are skipped).

Using **Ctrl+s** *won't* trigger the save logic for exercises — you'll have to type and execute the script to be considered for saving the changes.

### 100 Page Python Intro

The exercise and quiz questions in this app have been adapted from my [100 Page Python Intro](https://github.com/learnbyexample/100_page_python_intro) ebook.

