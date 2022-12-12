# Linux CLI Text Processing Exercises

This TUI application includes 40 questions to test your CLI text processing skills.

> **Note**  
> This application is intended for exercises based on Linux CLI tools. You might still be able to solve the exercises on other platforms, but I'm not sure if it works.

# Installation

You'll need to install `textual` first. See [Textual documentation](https://textual.textualize.io/getting_started/) for more details about installation. After that, you can clone this repository and run the `cli_exercises.py` script. Adjust terminal dimensions as needed. Example instructions shown below, adjust them based on your preferences and OS.

```bash
$ python3 -m venv textual_apps
$ cd textual_apps
$ source bin/activate
$ pip install textual==0.5.0

$ git clone --depth 1 https://github.com/learnbyexample/TUI-apps.git
$ cd TUI-apps/CLI-Exercises
$ python cli_exercises.py
```

After pressing **Ctrl+n** twice, you should get a screen similar to the one shown below:

<p align="center"><img src="./cli_exercises.png" alt="Sample screenshot for CLI exercises" /></p>

# Guide

* Press **Ctrl+p** and **Ctrl+n** to navigate the questions list.
    * **Ctrl+←** and **Ctrl+→** can be used instead.
    * You can also click them using mouse from the footer.
* Type the command in the box below the question. Cursor focus is meant to be always within this box.
* Press **Enter** to execute the command.
    * `/bin/sh` is the shell used. So, features like `echo {1..3}` (brace expansion) won't work.
    * Output would be displayed below the command box.
    * If the output matches the expected results, the command box will turn *green* and a reference solution will also be shown.
    * Issues due to errors and timeout (about `2` seconds) will be displayed in *red*.
* Contents of the input file and expected output are shown at the bottom of the screen. You might have to scroll down to view longer files.
* Press **Ctrl+s** to show the reference solution if you are unable to solve an exercise.
* Press **Ctrl+t** to toggle between light and dark themes.
* Press **Ctrl+q** or **Ctrl+c** to quit the app.
* Navigating and editing in the command box:
    * Use mouse click to position the cursor anywhere you like
    * **←** move left by one character
    * **→** move right by one character
    * **Ctrl+a** move to the start of the line
    * **Ctrl+e** move to the end of the line
    * **Ctrl+w** delete backwards till whitespace boundary or start of the line
    * **Ctrl+f** delete forwards till whitespace boundary or end of the line
    * **Ctrl+u** delete backwards till start of the line
    * **Ctrl+k** delete forwards till start of the line
    * **Backspace** delete character to the left of the cursor
    * **Ctrl+d** delete character to the right of the cursor
* Use **Page Up** and **Page Down** (or mouse) to scroll.

> **Note**  
> Commands you have typed are automatically saved in `user_progress.json` (only when you press **Enter** to execute a command — navigating to another question and closing the app won't trigger the save logic). Theme choice is also saved. If you close the application and open it again, the first unsolved question will be displayed (i.e. already solved questions are skipped). If you use **Ctrl+s**, the solution *won't* be saved in `user_progress.json` — you'll have to navigate to another question and back (or close and open the app) to be considered for saving the changes. Once you have solved a question, only a different correct solution can override the previously saved command.

> **Warning**  
> There is no safeguard against the command you are executing. They are treated as if you typed them from a shell session. For example, `ls` will list the contents of the current directory.

## Video demo

https://user-images.githubusercontent.com/17766317/206649676-a913ad0d-1be7-430d-8978-98517347d86b.mp4

You can also view the [demo video on youtube](https://youtu.be/0ggfQzXeYJg).

# Ebooks

Exercises used in this application are based on [my programming ebooks](https://learnbyexample.github.io/books/).

# License

Code snippets are licensed under [MIT LICENSE](../LICENSE)

Exercise questions and associated files (like `questions.json`) are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

