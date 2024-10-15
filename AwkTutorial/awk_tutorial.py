from textual.app import App
from textual.binding import Binding
from textual.containers import VerticalScroll, Vertical
from textual.widgets import Footer, Label, Input
from textual.widgets import Markdown

import subprocess
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

class AwkTutorialApp(App):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = SCRIPT_DIR.joinpath('awk_tutorial.css')
    BINDINGS = [
        Binding('ctrl+p', 'previous', 'Previous', show=True),
        Binding('ctrl+n', 'next', 'Next', show=True),
        Binding('ctrl+r', 'reset', 'Reset', show=True),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
    ]

    def __init__(self):
        super().__init__()

        self.idx = 0
        self.tutorial_files = sorted(SCRIPT_DIR.joinpath('tutorial').glob('*.md'))
        self.max_idx = len(self.tutorial_files) - 1
        self.l_title = Label(id='title')
        self.v_tutorial = VerticalScroll()

    def compose(self):
        yield self.l_title
        with Vertical() as self.v_main:
            yield self.v_tutorial
        yield Footer()

    def on_mount(self):
        self.dark = False
        self.setup_tutorial()

    def on_input_submitted(self, event):
        cnt = int(event.input.name)
        self.i_cmd = self.i_cmds[cnt]
        self.l_cmd_output = self.l_cmd_outputs[cnt]
        self.process_user_cmd()

    def process_user_cmd(self):
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
                self.l_cmd_output.update(self.trim(result.stdout))
                self.l_cmd_output_style('gray', 'Output', '')

    def setup_tutorial(self):
        self.v_tutorial.remove()
        block = False
        s = ''
        cnt = 0
        self.i_cmds = []
        self.l_cmd_outputs = []
        tt_widgets = []
        with open(self.tutorial_files[self.idx]) as f:
            title = f'[b]({self.idx+1}/{self.max_idx+1}) {next(f)[2:-1]}'
            self.l_title.update(title)
            for line in f:
                if line.startswith('```'):
                    if block:
                        cb_widgets = []
                        for c in s.splitlines():
                            if c.startswith('#'):
                                cb_widgets.append(Label(c, classes='comment'))
                            elif c.startswith('$ '):
                                self.i_cmd = Input(classes='input',
                                                   name=str(cnt))
                                self.l_cmd_output = Label(classes='cmd_output',
                                                          markup=False)
                                cb_widgets.append(self.i_cmd)
                                cb_widgets.append(self.l_cmd_output)
                                self.i_cmds.append(self.i_cmd)
                                self.l_cmd_outputs.append(self.l_cmd_output)
                                self.set_cmd(c[2:])
                                if cnt == 0:
                                    self.i_cmd.focus()
                                cnt += 1
                        tt_widgets.append(Vertical(*cb_widgets, classes='codeblock'))
                    else:
                        tt_widgets.append(Markdown(s))
                    s = ''
                    block ^= True
                    continue
                s += line
            if s:
                tt_widgets.append(Markdown(s))
        self.v_tutorial = VerticalScroll(*tt_widgets)
        self.v_main.mount(self.v_tutorial)

    def set_cmd(self, cmd):
        self.i_cmd.value = cmd
        self.i_cmd.cursor_position = len(cmd)
        self.process_user_cmd()

    def trim(self, text):
        return text.removesuffix('\n')

    def l_cmd_output_style(self, color, title, subtitle):
        self.l_cmd_output.styles.color = color
        self.l_cmd_output.styles.border = ('round', color)
        self.l_cmd_output.border_title = title
        self.l_cmd_output.border_subtitle = subtitle

    def action_previous(self):
        if self.idx > 0:
            self.idx -= 1
            self.setup_tutorial()

    def action_next(self):
        if self.idx < self.max_idx:
            self.idx += 1
            self.setup_tutorial()

    def action_reset(self):
        self.setup_tutorial()

    def action_toggle_theme(self):
        self.dark = not self.dark

def main():
    os.chdir(SCRIPT_DIR.joinpath('example_files'))
    app = AwkTutorialApp()
    app.run()

if __name__ == '__main__':
    main()

