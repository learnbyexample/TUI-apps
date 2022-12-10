#!/usr/bin/env python

from setuptools import setup

setup(
    name='cli_exercises',
    version='0.0.1',
    description='This TUI application includes 40 questions to test your CLI text processing skills.',
    author='learnbyexample',
    url='https://github.com/learnbyexample/TUI-apps/tree/main/CLI-Exercises',
    install_requires=['textual==0.5.0'],
    entry_points = {
        'console_scripts': ['cli_exercises=cli_exercises:main'],
    }
)
