from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Label, Input, MarkdownViewer, Button
from textual.widgets import RadioButton, RadioSet, ContentSwitcher
from rich.markdown import Markdown

import json
import re
import regex
import os
from pathlib import Path

class PyRegexExercises(App):
    CSS_PATH = 'pyregex_exercises.css'
    BINDINGS = [
                Binding('ctrl+p', 'previous', 'Prev'),
                Binding('ctrl+n', 'next', 'Next'),
                Binding('ctrl+s', 'solution', 'Solution'),
                Binding('ctrl+t', 'toggle_theme', 'Theme'),
                Binding('ctrl+q', 'app.quit', 'Quit'),
                Binding('f1', 'app_guide', 'App Guide', show=False),
                Binding('f2', 'regex_exercises', 'Regex Exercises', show=False),
                Binding('ctrl+r', 'toggle_fmt', 'Format', show=False),
                Binding('ctrl+b', 'toggle_debug', 'Debug', show=False),
               ]

    def __init__(self):
        super().__init__()

        with open('questions.json', encoding='UTF-8') as f:
            self.questions = tuple(json.load(f).values())
        self.q_idx = 0
        self.q_max_idx = len(self.questions) - 1

        self.progress_file = 'user_progress.json'
        try:
            with open(self.progress_file, encoding='UTF-8') as f:
                self.user_progress = {int(k): v for k,v in json.load(f).items()}
        except FileNotFoundError:
            self.user_progress = {}
        else:
            for idx in range(self.q_max_idx + 1):
                if not self.user_progress.get(idx, ('', False))[1]:
                    break
            self.q_idx = idx

        self.l_question = Label('', id='question')
        placeholder = 'Add your solution here. Use ip to represent the input.'
        self.i_user_code = Input(placeholder=placeholder, id='input')
        self.v_code = Vertical(self.l_question, self.i_user_code, id='code')
        self.l_code_error = Label()

        self.v_left_col = Vertical(classes='list')
        self.v_right_col = Vertical(classes='list')
        self.h_columns = Horizontal(self.v_left_col, self.v_right_col,
                                    id='columns')

        self.l_ref_solution = Label(id='solution', markup=False)
        self.l_ref_solution.border_title = 'Reference Solution'

        self.error_types = (SyntaxError, TypeError, ValueError,
                            NameError, AttributeError, IndexError,
                            re.error, regex._regex_core.error)
        self.input_bg_color = 'gray'
        self.input_error_color = 'ansi_red'
        self.item_color = 'gray'
        self.item_solved_color = 'green'
        self.item_failed_color = 'red'
        self.debug_color = 'orange'

        self.eval_func = (self.ip_op, self.search)
        self.fmt_func = (str, repr)
        self.fmt_idx = self.user_progress.get(-2, 0)
        self.debug_on = self.user_progress.get(-3, False)

        self.rb_fmt = (RadioButton('str'), RadioButton('repr'))
        self.rb_fmt[self.fmt_idx].value = True
        self.rb_debug = (RadioButton('expected'), RadioButton('actual'))
        self.rb_debug[self.debug_on].value = True

        with open('app_guide.md', encoding='UTF-8') as f:
            self.m_view = MarkdownViewer(f.read(), show_table_of_contents=False)

        self.b_tabs = (Button('App Guide', name='guide', classes='buttons'),
                       Button('Python re(gex)? exercises', name='exercises',
                              classes='buttons', variant='warning'))


    def compose(self):
        with Horizontal(classes='container'):
            for button in self.b_tabs:
                yield button
        with ContentSwitcher(initial='exercises') as self.cs_tabs:  
            with VerticalScroll(id='exercises') as self.v_exercises:
                yield self.v_code
                with Horizontal(classes='container'):
                    with RadioSet(name='repr', classes='radio'):
                        for rb in self.rb_fmt:
                            yield rb
                    with RadioSet(name='debug', classes='radio'):
                        for rb in self.rb_debug:
                            yield rb
                yield self.h_columns
                yield self.l_ref_solution
            with Vertical(id='guide'):
                yield self.m_view
        yield Footer()

    def on_mount(self):
        self.app.dark = self.user_progress.get(-1, False)
        self.set_question()

    def on_button_pressed(self, event):
        name = event.button.name
        idx = int(name == 'exercises')
        self.b_tabs[idx].variant = 'warning'
        self.b_tabs[idx ^ 1].variant = 'default'
        self.cs_tabs.current = name

    def on_input_submitted(self, event):
        self.process_user_code()
        self.save_progress()

    def process_user_code(self):
        self.l_ref_solution_clear()
        self.solved = self.eval_func[self.func_search]()
        if self.solved:
            self.i_user_code.styles.background = self.item_solved_color
            self.show_solution()

    def search(self):
        self.l_code_error.remove()
        solved = True
        try:
            self.i_user_code.styles.background = self.input_bg_color
            for idx, label in enumerate(self.l_left_col):
                ip = self.left_col[idx]
                if eval(self.i_user_code.value):
                    label.styles.color = self.item_solved_color
                else:
                    label.styles.color = self.item_failed_color
                    solved = False
            for idx, label in enumerate(self.l_right_col):
                ip = self.right_col[idx]
                if not eval(self.i_user_code.value):
                    label.styles.color = self.item_solved_color
                else:
                    label.styles.color = self.item_failed_color
                    solved = False
        except self.error_types as e:
            self.l_code_error = Label(str(e), classes='error', markup=False)
            self.l_code_error.border_title = str(type(e).__name__)
            self.v_code.mount(self.l_code_error)
            self.i_user_code.styles.background = self.input_error_color
            solved = False
        return solved

    def ip_op(self):
        self.l_code_error.remove()
        solved = True
        try:
            self.i_user_code.styles.background = self.input_bg_color
            f = self.right_fmt_func()
            for idx, label in enumerate(self.l_left_col):
                ip = self.left_col[idx]
                if self.eval_left_col:
                    ip = eval(ip)
                op = str(eval(self.i_user_code.value))
                if op == self.right_col[idx]:
                    label.styles.color = self.item_solved_color
                    self.l_right_col[idx].update(f(op))
                    self.l_right_col[idx].styles.color = self.item_solved_color
                else:
                    label.styles.color = self.item_failed_color
                    self.l_right_col[idx].styles.color = self.item_failed_color
                    solved = False
                    if self.debug_on:
                        self.l_right_col[idx].update(f(op))
                        self.l_right_col[idx].styles.color = self.debug_color
                    else:
                        self.l_right_col[idx].update(f(self.right_col[idx]))
        except self.error_types as e:
            self.l_code_error = Label(str(e), classes='error', markup=False)
            self.l_code_error.border_title = str(type(e).__name__)
            self.v_code.mount(self.l_code_error)
            self.i_user_code.styles.background = self.input_error_color
            solved = False
        return solved

    def set_question(self):
        self.v_exercises.scroll_home(animate=False)
        self.l_ref_solution_clear()

        self.l_code_error.remove()
        self.v_left_col.remove()
        self.v_right_col.remove()
        self.v_left_col = Vertical(classes='list')
        self.v_right_col = Vertical(classes='list')
        self.h_columns.mount(self.v_left_col)
        self.h_columns.mount(self.v_right_col)

        self.l_question.update(
                Markdown(f'(Q:{self.q_idx+1}/{self.q_max_idx+1}) ' +
                         self.questions[self.q_idx]['question']))
        self.ref_solution = self.questions[self.q_idx]['Reference solution']
        self.fill = self.questions[self.q_idx]['fill']
        self.func_search = self.fill.startswith(('re.search(', 'regex.search(',
                                         're.fullmatch(', 'regex.fullmatch(',))

        self.left_col = self.questions[self.q_idx]['left column']
        s = self.left_col[0]
        self.eval_left_col = (s[0] == '[' and s[-1] == ']')
        self.right_col = self.questions[self.q_idx]['right column']

        def populate_list(col, items, container, d, f):
            items[:] = [Label(f(s), markup=False, expand=True,
                              classes='list_item')
                        for s in col]
            t = d[self.func_search]
            container.mount(Label(f'[b]{t}', expand=True, classes='list_title'))
            for label in items:
                label.styles.color = self.item_color
                container.mount(label)

        f = self.left_fmt_func()
        d = ('Input', 'Should match')
        self.l_left_col = []
        populate_list(self.left_col,
                      self.l_left_col,
                      self.v_left_col,
                      d, f)

        f = self.right_fmt_func()
        d = ('Output', 'Should NOT match')
        self.l_right_col = []
        populate_list(self.right_col,
                      self.l_right_col,
                      self.v_right_col,
                      d, f)

        if self.q_idx in self.user_progress:
            self.i_user_code.value = self.user_progress[self.q_idx][0]
            self.process_user_code()
        else:
            self.i_user_code.value = self.fill
            self.i_user_code.styles.background = self.input_bg_color
        self.i_user_code.focus()
        try:
            idx = self.i_user_code.value.index('(')
        except ValueError:
            self.i_user_code.cursor_position = len(self.i_user_code.value) - 1
        else:
            self.i_user_code.cursor_position = idx + 3

    def save_progress(self):
        code = self.i_user_code.value
        if self.q_idx in self.user_progress:
            if (self.user_progress[self.q_idx][0] == code
                or (self.user_progress[self.q_idx][1] and not self.solved)):
                return
        self.user_progress[self.q_idx] = [code, self.solved]
        self.write_progress_file()

    def write_progress_file(self):
        with open(self.progress_file, 'w', encoding='UTF-8') as f:
            json.dump(self.user_progress, f, indent=4)

    def action_previous(self):
        if self.q_idx > 0:
            self.q_idx -= 1
            self.set_question()

    def action_next(self):
        if self.q_idx < self.q_max_idx:
            self.q_idx += 1
            self.set_question()

    def l_ref_solution_clear(self):
        self.l_ref_solution.update('')
        self.l_ref_solution.styles.border = ('none', 'gray')

    def show_solution(self):
        self.l_ref_solution.update(self.ref_solution)
        self.l_ref_solution.styles.border = ('round', 'gray')

    def action_solution(self):
        self.show_solution()
        self.v_exercises.scroll_end(animate=False)

    def left_fmt_func(self):
        f = self.fmt_func[self.fmt_idx]
        if self.eval_left_col:
            f = self.fmt_func[0]
        return f

    def right_fmt_func(self):
        f = self.fmt_func[self.fmt_idx]
        s = self.right_col[0]
        if (s[0] == '[' and s[-1] == ']') or (s[0] == '{' and s[-1] == '}'):
            f = self.fmt_func[0]
        return f

    def on_radio_set_changed(self, event):
        if event.radio_set.name == 'repr':
            self.fmt_idx = event.radio_set.pressed_index
            f = self.left_fmt_func()
            for idx, label in enumerate(self.l_left_col):
                label.update(f(self.left_col[idx]))
            f = self.right_fmt_func()
            for idx, label in enumerate(self.l_right_col):
                label.update(f(self.right_col[idx]))
            if self.debug_on:
                self.process_user_code()
        elif event.radio_set.name == 'debug':
            self.debug_on = bool(event.radio_set.pressed_index)
            if not self.func_search:
                self.process_user_code()
        self.user_progress[-2] = self.fmt_idx
        self.user_progress[-3] = self.debug_on
        self.write_progress_file()

    def action_toggle_theme(self):
        self.app.dark ^= True
        self.user_progress[-1] = self.app.dark
        self.write_progress_file()

    def action_app_guide(self):
        self.b_tabs[0].press()

    def action_regex_exercises(self):
        self.b_tabs[1].press()

    def action_toggle_fmt(self):
        self.fmt_idx ^= 1
        self.rb_fmt[self.fmt_idx].value = True

    def action_toggle_debug(self):
        self.debug_on ^= True
        self.rb_debug[self.debug_on].value = True


def main():
    os.chdir(Path(__file__).parent.resolve())
    app = PyRegexExercises()
    app.run()

if __name__ == '__main__':
    main()

