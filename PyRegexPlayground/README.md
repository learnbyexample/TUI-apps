# Python re(gex)? playground

This TUI application is intended as an interactive playground for Python Regular Expressions. The app also includes a comprehensive cheatsheet and several interactive examples.

# Installation

This app is available on PyPI as [regexplayground](https://pypi.org/project/regexplayground/). Example installation instructions are shown below, adjust them based on your preferences and OS.

```bash
# virtual environment
$ python3 -m venv textual_apps
$ cd textual_apps
$ source bin/activate
$ pip install regexplayground

# launch the app
$ regexplayground
```

To run the app without having to enter the virtual environment again, add this alias to `.bashrc` (or equivalent):

```bash
# you'll have to change the path
alias regexplayground='/path/to/textual_apps/bin/regexplayground'
```

As an alternative to manually managing such virtual environments, you can use [https://github.com/pypa/pipx](https://github.com/pypa/pipx) instead:

```bash
$ pipx install regexplayground
$ regexplayground
```

As yet another alternative, you can install `textual==0.85.2` (see [Textual documentation](https://textual.textualize.io/getting_started/) for more details), clone this repository and run the `pyregex_playground.py` file.

Adjust the terminal dimensions for the widgets to appear properly, for example 84x25 (characters x lines). Here are some sample screenshots:

<p align="center"><img src="./pyregex_finditer.png" alt="Sample screenshot from the Playground screen" /></p>

<p align="center"><img src="./pyregex_examples.png" alt="Sample screenshot from the Interactive Examples screen" /></p><br>

# Guide

See [app_guide.md](./app_guide.md)

# Ebook

See my [Understanding Python re(gex)?](https://github.com/learnbyexample/py_regular_expressions) ebook to learn regular expressions with hundreds of examples and exercises.

# License

Code snippets are licensed under [MIT LICENSE](../LICENSE)

Explanations and associated files (like `cheatsheet.md`) are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

