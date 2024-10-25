from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Footer, Label, TextArea, Button
from textual.widgets import MarkdownViewer, ContentSwitcher, DirectoryTree
from textual.widgets import RadioButton, RadioSet
from rich.markdown import Markdown
from rich.markup import escape as rich_escape

import json
import subprocess
import re
import os
from pathlib import Path
from sys import executable as PYTHON

SCRIPT_DIR = Path(__file__).parent.resolve()

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
            text_b4_cursor = self.get_current_line()[:self.cursor_location[1]]
            if re.fullmatch(r'(?:    )+', text_b4_cursor):
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
    COMMAND_PALETTE_BINDING = 'f5'
    CSS_PATH = SCRIPT_DIR.joinpath('python_exercises.css')
    BINDINGS = [
        Binding('ctrl+r', 'run', 'Run', show=True),
        Binding('ctrl+l', 'reset', 'Reset', show=True),
        Binding('ctrl+s', 'show_solution', 'Solution', show=True),
        Binding('ctrl+p', 'previous', 'Previous', show=True),
        Binding('ctrl+n', 'next', 'Next', show=True),
        Binding('f1', 'app_guide', 'App Guide', show=False),
        Binding('f2', 'exercises', 'Python Exercises', show=False),
        Binding('f3', 'quiz', 'Quiz', show=False),
        Binding('f4', 'directory', 'Directory', show=False),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
    ]

    def __init__(self):
        super().__init__()

        self.l_exercise = Label(classes='question')
        with open(SCRIPT_DIR.joinpath('exercises.json'), encoding='UTF-8') as f:
            self.exercises = tuple(json.load(f).values())
        self.e_idx = 0
        self.e_max_idx = len(self.exercises) - 1

        self.code_themes = ('github_light', 'vscode_dark')
        self.t_script = SmartTextArea(id='script', language='python')
        self.t_script.tab_behavior = 'indent'

        self.l_output = Label(id='output', markup=False)
        self.l_output.styles.border_subtitle_align = 'left'
        self.t_ref_solution = TextArea(id='solution', language='python')
        self.t_ref_solution.read_only = True
        self.t_ref_solution.border_title = 'Reference Solution'
        self.t_viewfile = TextArea(id='viewfile', language='python')
        self.t_viewfile.read_only = True

        self.progress_file = SCRIPT_DIR.joinpath('exercise_progress.json')
        try:
            with open(self.progress_file, encoding='UTF-8') as f:
                self.exercise_progress = {int(k): v for k,v in json.load(f).items()}
        except FileNotFoundError:
            self.exercise_progress = {}
        else:
            for idx in range(self.e_max_idx + 1):
                if not self.exercise_progress.get(idx, False):
                    break
            self.e_idx = idx

        self.l_quiz = Label(classes='question')
        self.l_quiz_result = Label(id='quiz_result')
        self.rset_quiz = RadioSet(id='rset')
        self.rbuttons_quiz = [RadioButton()]
        self.b_submit = Button('Submit', name='submit', id='submit')
        self.quiz_blocks = Path.read_text(SCRIPT_DIR.joinpath('quiz.txt'),
                                      encoding='UTF-8').rstrip().split('\n\n')
        self.q_idx = 0
        self.q_max_idx = len(self.quiz_blocks) - 1
        self.q_correct_ans_count = 0
        self.quiz_progress_file = SCRIPT_DIR.joinpath('quiz_progress.json')
        try:
            with open(self.quiz_progress_file, encoding='UTF-8') as f:
                self.quiz_progress = {int(k): v for k,v in json.load(f).items()}
        except FileNotFoundError:
            self.quiz_progress = {}
        else:
            for idx in range(self.q_max_idx + 1):
                if idx not in self.quiz_progress:
                    break
            self.q_idx = idx
            self.q_correct_ans_count = self.quiz_progress[-1]

        self.user_scripts = SCRIPT_DIR.joinpath('user_scripts')
        Path.mkdir(self.user_scripts, exist_ok=True)

        with open(SCRIPT_DIR.joinpath('app_guide.md'), encoding='UTF-8') as f:
            self.m_view = MarkdownViewer(f.read(), show_table_of_contents=False)

        self.b_tabs = (Button('App Guide', name='guide', classes='buttons'),
                       Button('Python Exercises', name='exercises', classes='buttons'),
                       Button('Quiz', name='quiz', classes='buttons'),
                       Button('Directory', name='directory', classes='buttons'))

    def compose(self):
        with Horizontal(id='b_tabs'):
            for button in self.b_tabs:
                yield button
        with ContentSwitcher() as self.cs_tabs:  
            with VerticalScroll(id='exercises'):
                yield self.l_exercise
                yield self.t_script
                yield self.l_output
                yield self.t_ref_solution
            with VerticalScroll(id='quiz'):
                yield self.l_quiz
                yield self.rset_quiz
                yield self.b_submit
                yield self.l_quiz_result
            with Vertical(id='guide'):
                yield self.m_view
            with Horizontal(id='directory'):
                yield DirectoryTree('./', id='tree')
                with VerticalScroll():
                    yield self.t_viewfile
        yield Footer()

    def on_mount(self):
        self.dark = self.exercise_progress.get(-1, False)
        if self.exercise_progress.get(-2, 'exercises') == 'exercises':
            self.action_exercises()
        else:
            self.action_quiz()

    def action_run(self):
        if self.cs_tabs.current != 'exercises':
            if self.cs_tabs.current == 'quiz' and not self.b_submit.disabled:
                self.process_quiz()
            return

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
            self.t_script.theme = self.code_themes[self.dark]
            if result.returncode:
                self.l_output.update(result.stderr)
                self.l_output_style('red', 'Error!',
                                    f'Exit Status: {result.returncode}')
            else:
                s1 = result.stdout.removesuffix('\n')
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

    def set_exercise(self, reset=False):
        self.l_ref_solution_clear()
        self.solved = False
        self.show_solution = False
        self.l_exercise.update(Markdown(self.exercises[self.e_idx]['exercise']))
        self.l_exercise.border_title = f'{self.e_idx+1}/{self.e_max_idx+1}'
        self.e_file = self.exercises[self.e_idx]['e_file']
        self.py_file = self.user_scripts.joinpath(self.e_file)
        self.exp_op_txt = self.exercises[self.e_idx]['exp_op'].removesuffix('\n')
        
        if not reset and Path.exists(self.py_file):
            path = self.py_file
        else:
            path = SCRIPT_DIR.joinpath(f'exercises/{self.e_file}')
        self.t_script.text = self.read_file(path)
        self.t_script.theme = self.code_themes[self.dark]
        self.l_output.update('')
        self.l_output_style('gray', 'Output', '')
        self.t_script.focus(scroll_visible=False)

    def read_file(self, path):
        text = Path.read_text(path, encoding='UTF-8')
        return text.removesuffix('\n')

    def save_progress(self):
        self.exercise_progress[self.e_idx] = self.solved
        self.write_exercise_progress_file()

    def write_exercise_progress_file(self):
        with open(self.progress_file, 'w', encoding='UTF-8') as f:
            json.dump(self.exercise_progress, f, indent=2)

    def on_button_pressed(self, event):
        name = event.button.name
        if name == 'submit':
            self.process_quiz()
            return

        self.cs_tabs.current = name
        for b in self.b_tabs:
            b.variant = 'default'
        if name == 'guide':
            idx = 0
        elif name == 'exercises':
            idx = 1
            self.exercise_progress[-2] = 'exercises'
            self.write_exercise_progress_file()
            self.t_script.focus()
            self.set_exercise()
        elif name == 'quiz':
            idx = 2
            self.exercise_progress[-2] = 'quiz'
            self.write_exercise_progress_file()
            self.set_quiz()
        else:
            idx = 3
        self.b_tabs[idx].variant = 'warning'

    def on_directory_tree_file_selected(self, event):
        path = event.path
        self.t_viewfile.text = self.read_file(path)
        self.t_viewfile.border_title = str(path)

    def l_ref_solution_clear(self):
        self.t_ref_solution.text = ''
        self.t_ref_solution.styles.border = ('none', 'green')

    def action_reset(self):
        if self.cs_tabs.current == 'exercises':
            self.set_exercise(reset=True)

    def action_show_solution(self):
        if self.cs_tabs.current == 'exercises':
            self.show_solution ^= True
            if self.show_solution:
                solution = SCRIPT_DIR.joinpath(f'solutions/{self.e_file}')
                self.t_ref_solution.text = self.read_file(solution)
                self.t_ref_solution.styles.border = ('round', 'green')
            else:
                self.l_ref_solution_clear()

    def action_previous(self):
        if self.cs_tabs.current == 'exercises' and self.e_idx > 0:
            self.e_idx -= 1
            self.set_exercise()
        elif self.cs_tabs.current == 'quiz' and self.q_idx > 0:
            self.q_idx -= 1
            self.set_quiz()

    def action_next(self):
        if self.cs_tabs.current == 'exercises' and self.e_idx < self.e_max_idx:
            self.e_idx += 1
            self.set_exercise()
        elif self.cs_tabs.current == 'quiz' and self.q_idx < self.q_max_idx:
            self.q_idx += 1
            self.set_quiz()

    def set_quiz(self):
        quiz_block = self.quiz_blocks[self.q_idx]
        q_question, *q_choices = quiz_block.split('\n')
        self.q_answer_choice = q_choices.pop()
        self.q_answer_idx = ord(self.q_answer_choice) - 97
        self.l_quiz.update(q_question[q_question.find(' ')+1:])
        self.l_quiz.border_title = f'{self.q_idx+1}/{self.q_max_idx+1}'

        for rb in self.rbuttons_quiz:
            rb.remove()
        self.rbuttons_quiz = []
        for s in q_choices:
            rb = RadioButton(rich_escape(s))
            self.rbuttons_quiz.append(rb)
            self.rset_quiz.mount(rb)
        self.b_submit.disabled = True

        if self.q_idx in self.quiz_progress:
            self.quiz_already_answered = True
            idx = self.quiz_progress[self.q_idx]
            self.rbuttons_quiz[idx].value = True
            self.quiz_submitted_idx = idx
            self.process_quiz()
        else:
            self.quiz_already_answered = False
            self.rset_quiz.disabled = False
            self.l_quiz_result.update('')
            self.b_submit.variant = 'primary'
            self.rset_quiz.focus()

    def process_quiz(self):
        if self.quiz_submitted_idx == self.q_answer_idx:
            text = '✅ You got that right!'
            if not self.quiz_already_answered:
                self.q_correct_ans_count += 1
        else:
            text = f'❌ Oops! The correct choice is: {self.q_answer_choice}'

        self.l_quiz_result.update(f'{text}\nCorrectly answered: '
                                  f'{self.q_correct_ans_count}/{self.q_max_idx+1}')
        self.rbuttons_quiz[self.q_answer_idx].styles.color = 'green'
        self.rbuttons_quiz[self.q_answer_idx].styles.text_style = 'bold'
        self.rset_quiz.disabled = True
        self.b_submit.disabled = True
        self.b_submit.variant = 'default'
        if not self.quiz_already_answered:
            self.write_quiz_progress_file()

    def write_quiz_progress_file(self):
        self.quiz_progress[self.q_idx] = self.quiz_submitted_idx
        self.quiz_progress[-1] = self.q_correct_ans_count
        with open(self.quiz_progress_file, 'w', encoding='UTF-8') as f:
            json.dump(self.quiz_progress, f, indent=2)

    def on_radio_set_changed(self, event):
        if not self.quiz_already_answered:
            self.quiz_submitted_idx = event.radio_set.pressed_index
            self.b_submit.disabled = False

    def action_app_guide(self):
        self.b_tabs[0].press()

    def action_exercises(self):
        self.b_tabs[1].press()

    def action_quiz(self):
        self.b_tabs[2].press()

    def action_directory(self):
        self.b_tabs[3].press()

    def action_toggle_theme(self):
        self.dark = not self.dark
        self.t_script.theme = self.code_themes[self.dark]
        self.t_ref_solution.theme = self.code_themes[self.dark]
        self.t_viewfile.theme = self.code_themes[self.dark]
        self.exercise_progress[-1] = self.dark
        self.write_exercise_progress_file()

def main():
    os.chdir(SCRIPT_DIR)
    app = PythonExercisesApp()
    app.run()

if __name__ == '__main__':
    main()
