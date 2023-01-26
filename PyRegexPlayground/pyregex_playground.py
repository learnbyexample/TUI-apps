from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Footer, Label, Input
from rich.panel import Panel
from rich.markup import escape
from rich.text import Text

import re
from functools import partial

class PyRegexPlayground(App):
    CSS_PATH = 'pyregex_playground.css'
    BINDINGS = [
        Binding('ctrl+r', 'replace', 'Replace', show=True),
        Binding('ctrl+p', 'prettify', 'Prettify', show=True),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
    ]

    def __init__(self):
        super().__init__()

        self.l_search = Label('Search', id='l_search')
        self.l_replace = Label('Replace', id='l_replace')

        self.data = ('Apple Banana Cherry\n'
                     'coffee\t: 150g\n'
                     'tea\t: 50g\n'
                     'sugar\t: 10g\n'
                     'Dragon Unicorn Centaur')
        self.prettify = True

        self.l_input = Label(id='l_input')
        self.l_input.update(Panel(self.data,
                                  title='Input',
                                  title_align='center'))

        self.l_output = Label(id='l_output')
        self.l_output.update(Panel('',
                                   title='Output',
                                   title_align='center'))

        placeholder = 'Search pattern. Press Enter to execute the command.'
        self.i_search = Input(placeholder=placeholder)
        self.i_search.styles.background = 'lightgray'
        placeholder = 'Replace pattern. Press Enter to execute the command.'
        self.i_replace = Input(placeholder=placeholder)
        self.i_replace.styles.background = 'lightgray'

    def compose(self):
        yield Label('[b]Python re(gex)? playground', id='header')
        yield Horizontal(self.l_search, self.i_search, id='h_search')
        self.h_replace = Horizontal(self.l_replace, self.i_replace, id='h_replace')
        yield self.h_replace
        yield self.l_input
        yield self.l_output
        yield Footer()

    def on_mount(self):
        self.dark = False
        self.h_replace.visible = False
        self.l_output.visible = self.h_replace.visible

    async def on_input_submitted(self, message):
        self.execute()

    def execute(self):
        self.execute_search()
        if self.h_replace.visible:
            self.execute_replace()

    def substitute(self, ip, pat, color):
        # need to take care of rich markup in data/patterns
        # or find another way to color
        if self.prettify:
            pat = f'[b][{color}]{pat}[/{color}][/b]'

        try:
            ip.styles.background = 'lightgray'
            op = re.sub(self.i_search.value, pat, self.data)
            return Text.from_markup(op) if self.prettify else op
        except re.error:
            ip.styles.background = 'red'
            return self.data

    def execute_search(self):
        op = self.substitute(self.i_search, r'\g<0>', 'red')
        self.l_input.update(Panel(op, title='Input', title_align='center'))

    def execute_replace(self):
        op = self.substitute(self.i_replace, self.i_replace.value, 'green')
        self.l_output.update(Panel(op, title='Output', title_align='center'))

    def action_replace(self):
        self.h_replace.visible = not self.h_replace.visible
        self.l_output.visible = self.h_replace.visible
        self.execute_replace()

    def action_prettify(self):
        self.prettify = not self.prettify
        self.execute()

    def action_toggle_theme(self):
        self.dark = not self.dark

if __name__ == '__main__':
    app = PyRegexPlayground()
    app.run()

