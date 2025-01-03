from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Footer, Label, Input, Button
from textual.widgets import MarkdownViewer, ContentSwitcher, DirectoryTree
from rich.markup import escape as rich_escape

import json
import subprocess
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

class GrepExercisesApp(App):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = SCRIPT_DIR.joinpath('grep_exercises.css')
    BINDINGS = [
        Binding('ctrl+s', 'show_solution', 'Solution', show=True),
        Binding('ctrl+p', 'previous', 'Previous', show=True),
        Binding('ctrl+n', 'next', 'Next', show=True),
        Binding('f1', 'app_guide', 'App Guide', show=False),
        Binding('f2', 'grep_exercises', 'Grep Exercises', show=False),
        Binding('f3', 'directory', 'Directory', show=False),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
    ]

    def __init__(self):
        super().__init__()

        Path('backups/text').mkdir(exist_ok=True)
        links = [Path('hello.py'), Path('backups/text/pat.txt')]
        targets = [Path('projects/python/hello.py'), Path('../../patterns.txt')]
        for link, target in zip(links, targets):
            if not link.is_file():
                link.symlink_to(target)
        for path in Path('.').rglob('*.pyc'):
            path.unlink()
        for path in Path('.').rglob('__pycache__'):
            path.rmdir()

        self.l_question = Label(id='question')
        with open(SCRIPT_DIR.joinpath('questions.json'), encoding='ascii') as f:
            self.questions = tuple(json.load(f).values())
        self.q_idx = 0
        self.q_max_idx = len(self.questions) - 1

        placeholder = 'Type your command here. Press Enter to execute the command.'
        self.i_cmd = Input(placeholder=placeholder)
        self.l_cmd_output = Label(id='cmd_output', markup=False)
        self.l_cmd_output.styles.border_subtitle_align = 'left'
        self.l_ref_solution = Label(id='solution', markup=False)
        self.l_ref_solution.border_title = 'Reference Solutions'
        self.h_ip_op = Horizontal(classes='container')
        self.l_viewfile = Label('', id='viewfile', expand=True, markup=False)

        self.progress_file = SCRIPT_DIR.joinpath('user_progress.json')
        try:
            with open(self.progress_file, encoding='ascii') as f:
                self.user_progress = {int(k): v for k,v in json.load(f).items()}
        except FileNotFoundError:
            self.user_progress = {}
        else:
            for idx in range(self.q_max_idx + 1):
                if not self.user_progress.get(idx, ('', False))[1]:
                    break
            self.q_idx = idx

        with open(SCRIPT_DIR.joinpath('app_guide.md'), encoding='UTF-8') as f:
            self.m_view = MarkdownViewer(f.read(), show_table_of_contents=False)

        self.b_tabs = (Button('App Guide', name='guide', classes='buttons'),
                       Button('Grep Exercises', name='exercises',
                              classes='buttons', variant='warning'),
                       Button('Directory', name='directory', classes='buttons'))

    def compose(self):
        with Horizontal(classes='container'):
            for button in self.b_tabs:
                yield button
        with ContentSwitcher(initial='exercises') as self.cs_tabs:  
            with VerticalScroll(id='exercises') as self.v_exercises:
                yield self.l_question
                yield self.i_cmd
                yield self.l_cmd_output
                yield self.l_ref_solution
                yield self.h_ip_op
            with Vertical(id='guide'):
                yield self.m_view
            with Horizontal(id='directory'):
                yield DirectoryTree('./', id='tree')
                with VerticalScroll():
                    yield self.l_viewfile
        yield Footer()

    def on_mount(self):
        self.dark = self.user_progress.get(-1, False)
        self.set_quest_ip_op()

    def on_input_submitted(self, event):
        self.process_user_cmd()

    def process_user_cmd(self):
        self.l_ref_solution_clear()
        self.solved = False
        try:
            result = subprocess.run(self.i_cmd.value, timeout=2,
                                    shell=True, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            msg = ('App might become unresponsive.\n'
                   'Wait a few seconds...\n'
                   'Or, press Ctrl+C to quit (press multiple times if needed).')
            self.l_cmd_output.update(msg)
            self.l_cmd_output_style('red', 'Oops, command timed out!!!', '')
            self.i_cmd.styles.background = 'palevioletred'
        else:
            if result.returncode:
                self.l_cmd_output.update(result.stderr)
                self.l_cmd_output_style('red', 'Error!',
                                  f'Exit Status: {result.returncode}')
                self.i_cmd.styles.background = 'lightgray'
            else:
                s1 = self.trim(result.stdout)
                s2 = self.op_txt
                self.l_cmd_output.update(s1)
                self.l_cmd_output_style('gray', 'Output', '')
                if self.questions[self.q_idx]['sort_op']:
                    s1 = sorted(s1.splitlines())
                    s2 = sorted(s2.splitlines())
                if s1 == s2:
                    self.i_cmd.styles.background = 'green'
                    self.solved = True
                    self.action_show_solution()
                    self.show_solution = True
                else:
                    self.i_cmd.styles.background = 'lightgray'
            self.save_progress()

    def l_cmd_output_style(self, color, title, subtitle):
        self.l_cmd_output.styles.color = color
        self.l_cmd_output.styles.border = ('round', color)
        self.l_cmd_output.border_title = title
        self.l_cmd_output.border_subtitle = subtitle

    def set_quest_ip_op(self):
        self.l_ref_solution_clear()
        self.solved = False
        self.l_question.update(self.style_inline_code(
                f'(Q:{self.q_idx+1}/{self.q_max_idx+1}) ' +
                self.questions[self.q_idx]['question']))
        self.ref_solution = self.questions[self.q_idx]['ref_solution']
        self.show_solution = False

        self.h_ip_op.remove()
        ip_files = self.questions[self.q_idx]['ip_file']
        v_ip_widgets = []
        for ip_file in ip_files:
            with open(ip_file, encoding='ascii') as f:
                ip_txt = self.trim(f.read())
            l_ip = Label(ip_txt, classes='ip_op', markup=False)
            l_ip.border_title = ip_file
            v_ip_widgets.append(l_ip)

        self.op_txt = self.trim(self.questions[self.q_idx]['op_file'])
        l_op = Label(self.op_txt, classes='ip_op', markup=False)
        l_op.border_title = 'Expected output'

        v_ip = Vertical(*v_ip_widgets, classes='ip_op_container')
        v_op = Vertical(l_op, classes='ip_op_container')
        if ip_files:
            self.h_ip_op = Horizontal(v_ip, v_op, classes='container')
        else:
            self.h_ip_op = v_op
        self.v_exercises.mount(self.h_ip_op)

        if self.q_idx in self.user_progress:
            self.set_cmd(self.user_progress[self.q_idx][0])
        else:
            self.i_cmd.value = ''
            self.i_cmd.styles.background = 'lightgray'
            self.l_cmd_output.update('')
            self.l_cmd_output_style('gray', 'Output', '')
        self.i_cmd.focus()

    def set_cmd(self, cmd):
        self.i_cmd.value = cmd
        self.i_cmd.cursor_position = len(cmd)
        self.process_user_cmd()

    def trim(self, text):
        return text.removesuffix('\n')

    def save_progress(self):
        cmd = self.i_cmd.value
        if self.q_idx in self.user_progress:
            if (self.user_progress[self.q_idx][0] == cmd
                or (self.user_progress[self.q_idx][1] and not self.solved)):
                return
        self.user_progress[self.q_idx] = [cmd, self.solved]
        self.write_progress_file()

    def write_progress_file(self):
        with open(self.progress_file, 'w', encoding='ascii') as f:
            json.dump(self.user_progress, f, indent=2)

    def on_button_pressed(self, event):
        self.refresh_bindings()
        name = event.button.name
        self.cs_tabs.current = name
        for b in self.b_tabs:
            b.variant = 'default'
        if name == 'guide':
            idx = 0
        elif name == 'exercises':
            idx = 1
            self.i_cmd.focus()
        else:
            idx = 2
        self.b_tabs[idx].variant = 'warning'

    def on_directory_tree_file_selected(self, event):
        path = event.path
        with open(path, encoding='ascii') as f:
            self.l_viewfile.update(self.trim(f.read()))
            self.l_viewfile.border_title = str(path)

    def l_ref_solution_clear(self):
        self.l_ref_solution.update('')
        self.l_ref_solution.styles.border = ('none', 'green')

    def action_show_solution(self):
        self.show_solution ^= True
        if self.show_solution:
            self.l_ref_solution.update('\n'.join(self.ref_solution))
            self.l_ref_solution.styles.border = ('round', 'green')
        else:
            self.l_ref_solution_clear()

    def style_inline_code(self, s):
        return re.sub(r'`([^`]+)`', r'[dark_orange3 on grey84]\1[/]',
                      rich_escape(s))

    def check_action(self, action, parameters):
        tab = self.cs_tabs.current
        if action in ('previous', 'next', 'show_solution') and tab != 'exercises':
            return False
        return True

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

    def action_grep_exercises(self):
        self.b_tabs[1].press()

    def action_directory(self):
        self.b_tabs[2].press()

    def action_toggle_theme(self):
        self.dark = not self.dark
        self.user_progress[-1] = self.dark
        self.write_progress_file()


def main():
    os.chdir(SCRIPT_DIR.joinpath('sample_input'))
    app = GrepExercisesApp()
    app.run()

if __name__ == '__main__':
    main()
