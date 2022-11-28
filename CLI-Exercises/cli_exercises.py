from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Button, Footer, Label, Input
from rich.panel import Panel

import json
import asyncio
import os
import subprocess
from functools import partial

class CLIExercisesApp(App):
    CSS_PATH = 'cli_exercises.css'
    BINDINGS = [
        Binding('ctrl+s', 'show_answer', 'Show Answer', show=True),
        ('ctrl+c,ctrl+q', 'quit', 'Quit'),
        Binding('ctrl+p', 'previous', 'Previous', show=False),
        Binding('ctrl+n', 'next', 'Next', show=False),
        ('ctrl+t', 'toggle_dark', 'Toggle theme'),
    ]

    def __init__(self):
        super().__init__()
        with open('questions.json') as f:
            all_questions = json.load(f)
        self.questions = tuple(v for k, v in all_questions.items())
        self.q_idx = 0
        self.q_max_idx = len(self.questions) - 1

        self.question = Label(id='question')
        self.sample_input = Label(id='sample_input')
        self.expected_output = Label(id='expected_output')

        self.previous = Button('←', id='previous', variant='success')
        self.next = Button('→', id='next', variant='success')
        
        placeholder = 'Type your command here. Press Enter to execute the command.'
        self.user_cmd_input = Input(placeholder=placeholder, id='user_cmd_input')
        self.user_cmd_output = Label(id='user_cmd_output')
        self.op_panel = partial(Panel, title='Output', title_align='left')

        self.progress_file = 'user_progress.json'
        if os.path.isfile(self.progress_file):
            with open(self.progress_file) as f:
                self.user_progress = json.load(f)
            for idx in range(self.q_max_idx):
                if self.user_progress.get(str(idx), ('', False))[1]:
                    self.q_idx = idx + 1
                else:
                    break
        else:
            self.user_progress = {}

    def compose(self):
        yield Label('[b]Linux CLI Text Processing Exercises', id='header')
        yield Container(self.previous, self.question, self.next,
                        id='question_container')
        yield self.user_cmd_input
        yield self.user_cmd_output
        yield Container(self.sample_input, self.expected_output, id='ip_op')
        yield Footer()

    def on_mount(self):
        self.dark = False
        self.set_quest_ip_op()

    async def on_input_submitted(self, message):
        self.process_user_cmd()

    def process_user_cmd(self):
        cmd = self.user_cmd_input.value
        if not self.show_answer_clicked:
            self.cmd_entered_by_user = cmd
        self.answered_correctly = False
        try:
            result = subprocess.run(cmd, timeout=2,
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
                                f"{self.questions[self.q_idx]['ref_solution']}")
                    panel = self.op_panel(result.stdout,
                                          subtitle=solution,
                                          subtitle_align='left')
                    self.user_cmd_output.update(panel)
                else:
                    self.user_cmd_input.styles.background = 'lightgray'
                    self.user_cmd_output.update(self.op_panel(result.stdout))

    def set_quest_ip_op(self):
        self.cmd_entered_by_user = ''
        self.show_answer_clicked = False
        self.update_button_state()
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

        self.q_idx_str = str(self.q_idx)
        if self.q_idx_str in self.user_progress:
            self.set_cmd(self.user_progress[self.q_idx_str][0])
        else:
            self.user_cmd_input.value = ''
            self.user_cmd_input.styles.background = 'lightgray'
            self.user_cmd_output.update(self.op_panel(''))
            self.user_cmd_output.styles.color = 'gray'

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id == 'previous':
            self.previous_quest()
        elif button_id == 'next':
            self.next_quest()

    def previous_quest(self):
        self.save_progress()
        self.q_idx -= 1
        self.set_quest_ip_op()

    def next_quest(self):
        self.save_progress()
        self.q_idx += 1
        self.set_quest_ip_op()

    def update_button_state(self):
        self.previous.disabled = False
        self.next.disabled = False
        if self.q_idx == 0:
            self.previous.disabled = True
        if self.q_idx == self.q_max_idx:
            self.next.disabled = True

    def save_progress(self):
        cmd = self.cmd_entered_by_user
        if cmd:
            if self.q_idx_str in self.user_progress:
                if (self.user_progress[self.q_idx_str][0] == cmd
                    or (self.user_progress[self.q_idx_str][1]
                        and not self.answered_correctly)):
                    return
            self.user_progress[self.q_idx_str] = [cmd, self.answered_correctly]
            with open(self.progress_file, 'w') as f:
                f.write(json.dumps(self.user_progress, indent=4))

    def action_show_answer(self):
        self.show_answer_clicked = True
        self.set_cmd(self.questions[self.q_idx]['ref_solution'])

    def set_cmd(self, cmd):
        self.user_cmd_input.value = cmd
        self.user_cmd_input.cursor_position = len(cmd)
        self.process_user_cmd()

    def action_previous(self):
        if not self.previous.disabled:
            self.previous_quest()

    def action_next(self):
        if not self.next.disabled:
            self.next_quest()

    def action_toggle_dark(self):
        self.dark = not self.dark

    def action_quit(self):
        self.save_progress()
        app.exit()


if __name__ == '__main__':
    app = CLIExercisesApp()
    app.run()

