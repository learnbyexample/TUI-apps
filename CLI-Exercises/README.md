# Linux CLI Text Processing Exercises

This TUI application includes 70+ questions to test your CLI text processing skills.

> **Note**  
> This application is intended for exercises based on Linux CLI tools. You might still be able to solve the exercises on other platforms, but I'm not sure if it works.

# Installation

This app is available on PyPI as [cliexercises](https://pypi.org/project/cliexercises/). Example installation instructions are shown below, adjust them based on your preferences and OS.

```bash
# virtual environment
$ python3 -m venv textual_apps
$ cd textual_apps
$ source bin/activate
$ pip install cliexercises

# launch the app
$ cliexercises
```

To run the app without having to enter the virtual environment again, add this alias to `.bashrc` (or equivalent):

```bash
# you'll have to change the path
alias cliexercises='/path/to/textual_apps/bin/cliexercises'
```

As an alternative to manually managing such virtual environments, you can use [https://github.com/pypa/pipx](https://github.com/pypa/pipx) instead:

```bash
$ pipx install cliexercises
$ cliexercises
```

As yet another alternative, you can install `textual==0.85.2` (see [Textual documentation](https://textual.textualize.io/getting_started/) for more details), clone this repository and run the `cli_exercises.py` file.

Adjust the terminal dimensions for the widgets to appear properly, for example 84x25 (characters x lines). Here's a sample screenshot:

<p align="center"><img src="./cli_exercises.png" alt="Sample screenshot for CLI exercises" /></p>

# Guide

See [app_guide.md](./app_guide.md)

# Video demo

You can view a demo video about this app on Youtube: [https://youtu.be/lcm_F7zPzRY](https://youtu.be/lcm_F7zPzRY)

# License

Code snippets are licensed under [MIT LICENSE](../LICENSE)

Exercise questions and associated files (like `questions.json`) are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

