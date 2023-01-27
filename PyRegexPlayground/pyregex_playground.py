from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Footer, Label, Input
from rich.panel import Panel
from rich.text import Text
from rich.pretty import Pretty

import re
from functools import partial

class PyRegexPlayground(App):
    CSS_PATH = 'pyregex_playground.css'
    BINDINGS = [
        Binding('ctrl+u', 'update_ip', 'Update ip', show=True),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
    ]

    def __init__(self):
        super().__init__()

        self.l_compile = Label('Compile', id='l_compile')
        self.l_action = Label('Action', id='l_action')

        self.read_data()
        self.l_input = Label(id='l_input')
        self.ip_panel = partial(Panel, title='ip', title_align='center')
        self.l_input.update(self.ip_panel(self.data))

        self.l_output = Label(id='l_output')
        self.op_panel = partial(Panel, title='Output', title_align='center')
        self.l_output.update(self.op_panel(''))

        placeholder = 'Search pattern. Press Enter to compile.'
        self.i_compile = Input(placeholder=placeholder, value="re.compile(r'')")
        self.i_compile.styles.background = 'lightgray'
        placeholder = "Function to run. Example: pat.sub(r'X', ip)"
        self.i_action = Input(placeholder=placeholder)
        self.i_action.styles.background = 'lightgray'

        self.error_types = (re.error, SyntaxError, TypeError, ValueError,
                            NameError, AttributeError)

    def compose(self):
        yield Label('[b]Python re(gex)? playground', id='header')
        yield Horizontal(self.l_compile, self.i_compile, id='h_compile')
        yield self.l_input
        yield Horizontal(self.l_action, self.i_action, id='h_action')
        yield self.l_output
        yield Footer()

    def on_mount(self):
        self.dark = False
        self.i_compile.focus()
        self.i_compile.cursor_position = len(self.i_compile.value) - 2

    async def on_input_submitted(self, message):
        ip = self.data
        try:
            self.i_compile.styles.background = 'lightgray'
            pat = eval(self.i_compile.value)
        except self.error_types:
            self.i_compile.styles.background = 'red'
        else:
            op = Text(ip)
            for m in pat.finditer(ip):
                op.stylize('bold red', *m.span())
            self.l_input.update(self.ip_panel(op))

        if self.i_action.value:
            try:
                self.i_action.styles.background = 'lightgray'
                op = eval(self.i_action.value)
            except self.error_types:
                self.i_action.styles.background = 'red'
            else:
                if type(op) != str:
                    op = Pretty(op)
                self.l_output.update(self.op_panel(op))

    def read_data(self):
        with open('ip.txt') as f:
            self.data = f.read()

    def action_update_ip(self):
        self.read_data()
        self.l_input.update(self.ip_panel(self.data))

    def action_toggle_theme(self):
        self.dark = not self.dark

if __name__ == '__main__':
    app = PyRegexPlayground()
    app.run()

