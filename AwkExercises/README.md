# Awk Exercises

This TUI application includes 80+ questions meant to be solved using `GNU awk`. Some exercises will require you to combine `awk` with other CLI tools such as `tac`.

> **Note**  
> This application is intended to be run in a Linux-like environment. You might still be able to solve the exercises on other platforms, but I do not know if that'll work.

# Installation

This app is available on PyPI as [awkexercises](https://pypi.org/project/awkexercises/). Example installation instructions are shown below, adjust them based on your preferences and OS.

```bash
# virtual environment
$ python3 -m venv textual_apps
$ cd textual_apps
$ source bin/activate
$ pip install awkexercises

# launch the app
$ awkexercises
```

To run the app without having to enter the virtual environment again, add this alias to `.bashrc` (or equivalent):

```bash
# you'll have to change the path
alias awkexercises='/path/to/textual_apps/bin/awkexercises'
```

As an alternative to manually managing such virtual environments, you can use [https://github.com/pypa/pipx](https://github.com/pypa/pipx) instead:

```bash
$ pipx install awkexercises
$ awkexercises
```

As yet another alternative, you can install `textual==0.85.2` (see [Textual documentation](https://textual.textualize.io/getting_started/) for more details), clone this repository and run the `awk_exercises.py` file.

Adjust the terminal dimensions for the widgets to appear properly, for example 84x25 (characters x lines). Here's a sample screenshot:

<p align="center"><img src="./awk_exercises.png" alt="Sample screenshot for Awk exercises" /></p>

# Guide

See [app_guide.md](./app_guide.md)

# Ebook

See my [CLI text processing with GNU awk](https://github.com/learnbyexample/learn_gnuawk) ebook to learn `GNU awk` with hundreds of examples and exercises.

# License

Code snippets are licensed under [MIT LICENSE](../LICENSE)

Exercise questions and associated files (like `questions.json`) are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

