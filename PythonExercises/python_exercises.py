from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Footer, Label, TextArea, Button
from textual.widgets import MarkdownViewer, ContentSwitcher, DirectoryTree
from rich.markdown import Markdown

import json
import subprocess
import re
import os
from pathlib import Path
from sys import executable as PYTHON

SCRIPT_DIR = Path(__file__).parent.resolve()
# syntax highlight only for py files

class SmartTextArea(TextArea):
    BINDINGS = [
        Binding('ctrl+d', 'dup_line', 'duplicate current line', show=False),
        Binding('ctrl+o', 'open_line', 'open new line below', show=False),
    ]

    def _on_key(self, event):
        if event.key == 'enter':
            self.insert_indentation()
            event.prevent_default()
        elif event.key == 'backspace':
            m = re.fullmatch(r' +', self.get_current_line())
            if m and len(m[0]) % 4 == 0:
                self.action_delete_left()
                self.action_delete_left()
                self.action_delete_left()

    def get_current_line(self):
        return self.document.get_line(self.cursor_location[0])

    def insert_indentation(self):
        m = re.search(r'\A( *)(\w+\b)?', self.get_current_line())
        n = len(m[1])
        if n % 4 != 0:
            n = 0
        self.insert(f'\n{" " * n}')
        if m[2] in ('def', 'for', 'if', 'elif', 'else',
                    'with', 'while', 'try', 'except', 'finally',
                    'match', 'case', 'class', 'async'):
            self.insert('    ')

    def action_dup_line(self):
        self.action_cursor_line_start()
        self.insert(f'{self.get_current_line()}\n')

    def action_open_line(self):
        self.action_cursor_line_end()
        self.insert_indentation()

class PythonExercisesApp(App):
    COMMAND_PALETTE_BINDING = 'f4'
    CSS_PATH = SCRIPT_DIR.joinpath('python_exercises.css')
    BINDINGS = [
        Binding('ctrl+r', 'run', 'Run', show=True),
        Binding('ctrl+l', 'reset', 'Reset', show=True),
        Binding('ctrl+s', 'show_solution', 'Solution', show=True),
        Binding('ctrl+p', 'previous', 'Prev', show=True),
        Binding('ctrl+n', 'next', 'Next', show=True),
        Binding('f1', 'app_guide', 'App Guide', show=False),
        Binding('f2', 'python_exercises', 'Python Exercises', show=False),
        Binding('f3', 'directory', 'Directory', show=False),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
    ]

    def __init__(self):
        super().__init__()

        self.l_question = Label(id='question')
        with open(SCRIPT_DIR.joinpath('questions.json'), encoding='UTF-8') as f:
            self.questions = tuple(json.load(f).values())
        self.q_idx = 0
        self.q_max_idx = len(self.questions) - 1

        self.themes = ('github_light', 'vscode_dark')
        self.t_script = SmartTextArea(id='script', language='python')
        self.t_script.tab_behavior = 'indent'

        self.l_output = Label(id='output', markup=False)
        self.l_output.styles.border_subtitle_align = 'left'
        self.t_ref_solution = TextArea(id='solution', language='python')
        self.t_ref_solution.read_only = True
        self.t_ref_solution.border_title = 'Reference Solution'
        self.t_viewfile = TextArea(id='viewfile', language='python')
        self.t_viewfile.read_only = True

        self.progress_file = SCRIPT_DIR.joinpath('user_progress.json')
        try:
            with open(self.progress_file, encoding='UTF-8') as f:
                self.user_progress = {int(k): v for k,v in json.load(f).items()}
        except FileNotFoundError:
            self.user_progress = {}
        else:
            for idx in range(self.q_max_idx + 1):
                if not self.user_progress.get(idx, False):
                    break
            self.q_idx = idx

        self.user_scripts = SCRIPT_DIR.joinpath('user_scripts')
        Path.mkdir(self.user_scripts, exist_ok=True)

        with open(SCRIPT_DIR.joinpath('app_guide.md'), encoding='UTF-8') as f:
            self.m_view = MarkdownViewer(f.read(), show_table_of_contents=False)

        self.b_tabs = (Button('App Guide', name='guide', classes='buttons'),
                       Button('Python Exercises', name='exercises',
                              classes='buttons', variant='warning'),
                       Button('Directory', name='directory', classes='buttons'))

    def compose(self):
        with Horizontal(id='b_tabs'):
            for button in self.b_tabs:
                yield button
        with ContentSwitcher(initial='exercises') as self.cs_tabs:  
            with VerticalScroll(id='exercises') as self.v_exercises:
                yield self.l_question
                yield self.t_script
                yield self.l_output
                yield self.t_ref_solution
            with Vertical(id='guide'):
                yield self.m_view
            with Horizontal(id='directory'):
                yield DirectoryTree('./', id='tree')
                with VerticalScroll():
                    yield self.t_viewfile
        yield Footer()

    def on_mount(self):
        self.dark = self.user_progress.get(-1, False)
        self.set_quest_ip_op()

    def action_run(self):
        Path.write_text(self.py_file, f'{self.t_script.text}\n', encoding='UTF-8')
        try:
            result = subprocess.run(f'{PYTHON} {self.py_file}', timeout=5,
                                    shell=True, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            msg = ('App might become unresponsive.\n'
                   'Wait a few seconds...\n'
                   'Or, press Ctrl+C to quit (press multiple times if needed).')
            self.l_output.update(msg)
            self.l_output_style('red', 'Oops, command timed out!!!', '')
            self.t_script.styles.background = 'palevioletred'
        else:
            self.t_script.theme = self.themes[self.dark]
            if result.returncode:
                self.l_output.update(result.stderr)
                self.l_output_style('red', 'Error!',
                                    f'Exit Status: {result.returncode}')
            else:
                s1 = self.trim(result.stdout)
                s2 = self.exp_op_txt
                self.l_output.update(s1)
                self.l_output_style('gray', 'Output', '')
                if s1 == s2:
                    self.t_script.styles.background = 'lightgreen'
                    self.solved = True
                    self.show_solution = False
                    self.action_show_solution()
            self.save_progress()

    def l_output_style(self, color, title, subtitle):
        self.l_output.styles.color = color
        self.l_output.styles.border = ('round', color)
        self.l_output.border_title = title
        self.l_output.border_subtitle = subtitle

    def set_quest_ip_op(self, reset=False):
        self.l_ref_solution_clear()
        self.solved = False
        self.show_solution = False
        self.l_question.update(
                Markdown(f'(Q:{self.q_idx+1}/{self.q_max_idx+1}) ' +
                         self.questions[self.q_idx]['question']))
        self.q_file = self.questions[self.q_idx]['q_file']
        self.py_file = self.user_scripts.joinpath(self.q_file)
        self.exp_op_txt = self.trim(self.questions[self.q_idx]['exp_op'])
        
        if not reset and Path.exists(self.py_file):
            path = self.py_file
        else:
            path = SCRIPT_DIR.joinpath(f"questions/{self.q_file}")
        self.t_script.text = self.read_file(path)
        self.t_script.theme = self.themes[self.dark]
        self.l_output.update('')
        self.l_output_style('gray', 'Output', '')
        self.t_script.focus(scroll_visible=False)

    def read_file(self, path):
        text = Path.read_text(path, encoding='UTF-8')
        return self.trim(text)

    def trim(self, text):
        if text.endswith('\n'):
            text = text[:-1]
        return text

    def save_progress(self):
        self.user_progress[self.q_idx] = self.solved
        self.write_progress_file()

    def write_progress_file(self):
        with open(self.progress_file, 'w', encoding='UTF-8') as f:
            json.dump(self.user_progress, f, indent=2)

    def on_button_pressed(self, event):
        name = event.button.name
        self.cs_tabs.current = name
        for b in self.b_tabs:
            b.variant = 'default'
        if name == 'guide':
            idx = 0
        elif name == 'exercises':
            idx = 1
            self.t_script.focus()
        else:
            idx = 2
        self.b_tabs[idx].variant = 'warning'

    def on_directory_tree_file_selected(self, event):
        path = event.path
        #if path.suffix == '.md':
        #    self.t_viewfile.language = 'markdown'
        #else:
        #    self.t_viewfile.language = 'python'
        self.t_viewfile.text = self.read_file(path)
        self.t_viewfile.border_title = str(path)

    def l_ref_solution_clear(self):
        self.t_ref_solution.text = ''
        self.t_ref_solution.styles.border = ('none', 'green')

    def action_reset(self):
        self.set_quest_ip_op(reset=True)

    def action_show_solution(self):
        self.show_solution ^= True
        if self.show_solution:
            solution = SCRIPT_DIR.joinpath(f"solutions/{self.q_file}")
            self.t_ref_solution.text = self.read_file(solution)
            self.t_ref_solution.styles.border = ('round', 'green')
        else:
            self.l_ref_solution_clear()

    def action_previous(self):
        if self.q_idx > 0:
            self.q_idx -= 1
            self.set_quest_ip_op()

    def action_next(self):
        if self.q_idx < self.q_max_idx:
            self.q_idx += 1
            self.set_quest_ip_op()

    def action_app_guide(self):
        self.b_tabs[0].press()

    def action_python_exercises(self):
        self.b_tabs[1].press()

    def action_directory(self):
        self.b_tabs[2].press()

    def action_toggle_theme(self):
        self.dark = not self.dark
        self.t_script.theme = self.themes[self.dark]
        self.t_ref_solution.theme = self.themes[self.dark]
        self.t_viewfile.theme = self.themes[self.dark]
        self.user_progress[-1] = self.dark
        self.write_progress_file()


def main():
    os.chdir(SCRIPT_DIR)
    app = PythonExercisesApp()
    app.run()

if __name__ == '__main__':
    main()
