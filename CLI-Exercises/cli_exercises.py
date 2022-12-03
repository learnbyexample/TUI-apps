from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Button, Footer, Label, Input
from rich.panel import Panel
from rich.markup import escape

import json
import asyncio
import os
import subprocess
import re
from functools import partial

class CLIExercisesApp(App):
    CSS_PATH = 'cli_exercises.css'
    BINDINGS = [
        Binding('ctrl+s', 'show_answer', 'Solution', show=True),
        Binding('ctrl+p,ctrl+left', 'previous', 'Prev', show=True),
        Binding('ctrl+n,ctrl+right', 'next', 'Next', show=True),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
        Binding('ctrl+u', 'clear_till_start',
                'Clear till start of line', show=False),
        Binding('ctrl+k', 'clear_till_end',
                'Clear till end of line', show=False),
        Binding('ctrl+w', 'clear_till_prev_space',
                'Clear till previous space or start of line', show=False),
        Binding('ctrl+f', 'clear_till_next_space',
                'Clear till next space or end of line', show=False),
        Binding('ctrl+a', 'move_to_start',
                'Move cursor to start of line', show=False),
        Binding('ctrl+e', 'move_to_end',
                'Move cursor to end of line', show=False),
    ]

    def __init__(self):
        super().__init__()

        with open('questions.json') as f:
            self.questions = tuple(json.load(f).values())
        self.q_idx = 0
        self.q_max_idx = len(self.questions) - 1

        self.question = Label(id='question')
        self.sample_input = Label(id='sample_input')
        self.expected_output = Label(id='expected_output')

        placeholder = 'Type your command here. Press Enter to execute the command.'
        self.user_cmd_input = Input(placeholder=placeholder, id='user_cmd_input')
        self.user_cmd_output = Label(id='user_cmd_output')
        self.op_panel = partial(Panel, title='Output', title_align='left')

        self.progress_file = 'user_progress.json'
        if os.path.isfile(self.progress_file):
            with open(self.progress_file) as f:
                self.user_progress = {int(k): v for k,v in json.load(f).items()}
            for idx in range(self.q_max_idx + 1):
                if not self.user_progress.get(idx, ('', False))[1]:
                    break
            self.q_idx = idx
        else:
            self.user_progress = {}

    def compose(self):
        yield Label('[b]Linux CLI Text Processing Exercises', id='header')
        yield self.question
        yield self.user_cmd_input
        yield self.user_cmd_output
        yield Container(self.sample_input, self.expected_output, id='ip_op')
        yield Footer()

    def on_mount(self):
        self.dark = self.user_progress.get(-1, False)
        self.set_quest_ip_op()

    async def on_input_submitted(self, message):
        self.process_user_cmd()

    def process_user_cmd(self):
        self.answered_correctly = False
        try:
            result = subprocess.run(self.user_cmd_input.value, timeout=2,
                                    shell=True, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            msg = ('App might become unresponsive.\n'
                   'Wait a few seconds...\n'
                   'Or, press Ctrl+C to quit (press multiple times if needed).')
            panel = self.op_panel(msg, title='Oops, command timed out!!!')
            self.user_cmd_output.update(panel)
            self.user_cmd_output.styles.color = 'red'
            self.user_cmd_input.styles.background = 'palevioletred'
        else:
            if result.returncode:
                panel = self.op_panel(result.stderr,
                                      title='Error!',
                                      subtitle=f'Exit Status: {result.returncode}',
                                      subtitle_align='left')
                self.user_cmd_output.update(panel)
                self.user_cmd_output.styles.color = 'red'
                self.user_cmd_input.styles.background = 'lightgray'
            else:
                self.user_cmd_output.styles.color = 'gray'
                if result.stdout == self.op_txt:
                    if not self.show_answer_clicked:
                        self.answered_correctly = True
                    self.user_cmd_input.styles.background = 'green'
                    solution = (f"[b]Reference Solution:[/b] [green]"
                                f"{escape(self.questions[self.q_idx]['ref_solution'])}")
                    panel = self.op_panel(result.stdout,
                                          subtitle=solution,
                                          subtitle_align='left')
                    self.user_cmd_output.update(panel)
                else:
                    self.user_cmd_input.styles.background = 'lightgray'
                    self.user_cmd_output.update(self.op_panel(result.stdout))
            if not self.show_answer_clicked:
                self.save_progress()

    def set_quest_ip_op(self):
        self.answered_correctly = False
        self.show_answer_clicked = False
        quest = f"Q{self.q_idx + 1}) {self.questions[self.q_idx]['question']}"
        self.question.update(quest)

        ip_file = self.questions[self.q_idx]['ip_file']
        with open(ip_file) as f:
            ip_txt = f.read()
        self.sample_input.update(Panel(ip_txt,
                                       title=ip_file,
                                       title_align='center'))

        op_file = f"expected_output/{self.questions[self.q_idx]['op_file']}"
        with open(op_file) as f:
            self.op_txt = f.read()
        self.expected_output.update(Panel(self.op_txt,
                                          title='Expected output',
                                          title_align='center'))

        if self.q_idx in self.user_progress:
            self.set_cmd(self.user_progress[self.q_idx][0])
        else:
            self.user_cmd_input.value = ''
            self.user_cmd_input.styles.background = 'lightgray'
            self.user_cmd_output.update(self.op_panel(''))
            self.user_cmd_output.styles.color = 'gray'

        self.user_cmd_input.focus()

    def set_cmd(self, cmd):
        self.user_cmd_input.value = cmd
        self.user_cmd_input.cursor_position = len(cmd)
        self.process_user_cmd()

    def save_progress(self):
        cmd = self.user_cmd_input.value
        if self.q_idx in self.user_progress:
            if (self.user_progress[self.q_idx][0] == cmd
                or (self.user_progress[self.q_idx][1]
                    and not self.answered_correctly)):
                return
        self.user_progress[self.q_idx] = [cmd, self.answered_correctly]
        self.write_progress_file()

    def write_progress_file(self):
        with open(self.progress_file, 'w') as f:
            f.write(json.dumps(self.user_progress, indent=4))

    def action_show_answer(self):
        self.show_answer_clicked = True
        self.set_cmd(self.questions[self.q_idx]['ref_solution'])

    def action_previous(self):
        if self.q_idx > 0:
            self.q_idx -= 1
            self.set_quest_ip_op()

    def action_next(self):
        if self.q_idx < self.q_max_idx:
            self.q_idx += 1
            self.set_quest_ip_op()

    def action_toggle_theme(self):
        self.dark = not self.dark
        self.user_progress[-1] = self.dark
        self.write_progress_file()

    def action_clear_till_start(self):
        cmd = self.user_cmd_input.value[self.user_cmd_input.cursor_position:]
        self.user_cmd_input.value = cmd
        self.user_cmd_input.cursor_position = 0

    def action_clear_till_end(self):
        cmd = self.user_cmd_input.value[:self.user_cmd_input.cursor_position]
        self.user_cmd_input.value = cmd
        self.user_cmd_input.cursor_position = len(cmd)

    def action_clear_till_prev_space(self):
        cmd = self.user_cmd_input.value
        pos = self.user_cmd_input.cursor_position
        s = re.sub(r'\S*\s*$', '', cmd[:pos])
        self.user_cmd_input.value = s + cmd[pos:]
        self.user_cmd_input.cursor_position = len(s)

    def action_clear_till_next_space(self):
        cmd = self.user_cmd_input.value
        pos = self.user_cmd_input.cursor_position
        s = re.sub(r'^\s*\S*', '', cmd[pos:])
        self.user_cmd_input.value = cmd[:pos] + s
        self.user_cmd_input.cursor_position = pos

    def action_move_to_start(self):
        self.user_cmd_input.cursor_position = 0

    def action_move_to_end(self):
        self.user_cmd_input.cursor_position = len(self.user_cmd_input.value)


if __name__ == '__main__':
    app = CLIExercisesApp()
    app.run()

