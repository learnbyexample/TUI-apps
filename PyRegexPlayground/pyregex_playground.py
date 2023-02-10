from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Label, Input
from textual.screen import Screen
from rich.panel import Panel
from rich.text import Text
from rich.pretty import Pretty
from rich.markdown import Markdown
from rich.highlighter import Highlighter

import json
import re
from functools import partial
from math import factorial

HELP_TEXT = '''
You can type the search pattern in the [b]Compile[/b] input box and press the \
[b]Enter[/b] key to execute. For example, [b][green]re.compile(r'\d')[/green][/b] \
to match digit characters. Matching portions will be highlighted in red.

The compiled pattern is available via the [b][green]pat[/green][/b] variable \
and you can use [b][green]ip[/green][/b] to refer to the input string. You \
can transform or extract data by typing appropriate methods in the \
[b]Action[/b] box. For example, [b][green]pat.sub(r'(\g<0>)', ip)[/green][/b] \
will add parenthesis around the matching portions.

The input string is obtained from the [b][green]ip.txt[/green][/b] file. You \
can change contents of this file and press [b][red]Ctrl+u[/red][/b] to update \
the [b][green]ip[/green][/b] variable. You'll have to press [b]Enter[/b] again \
to update the results for the changed data.

Some of the error types are caught. In such cases, the background color of the \
input boxes will change to red and the error message will be displayed below \
the corresponding box. Other errors might result in the app crashing.

Press [b][red]Ctrl+t[/red][/b] to toggle the theme between light and dark modes.
'''

ERROR_TYPES = (re.error, SyntaxError, TypeError, ValueError,
               NameError, AttributeError)

class CommentHighlighter(Highlighter):
    def highlight(self, text):
        if str(text[0]) == '#':
            text.stylize('italic color(8)')


class Help(Screen):
    BINDINGS = [('escape', 'app.pop_screen', 'Pop screen')]

    def compose(self):
        yield Label(Panel(Text.from_markup(HELP_TEXT),
                          title='[b]Help[/b] (press Esc to go back)',
                          title_align='center'))


class Cheatsheet(Screen):
    BINDINGS = [('escape', 'app.pop_screen', 'Pop screen')]

    def compose(self):
        yield Label('[b]Cheatsheet[/b] (press Esc to go back)',
                    classes='header')
        self.v_cheatsheet = Vertical(classes='container')
        yield self.v_cheatsheet

    def on_mount(self):
        self.load_cheatsheet()

    async def on_input_submitted(self, event):
        idx = int(event.input.name)
        input_block = self.input_collection[idx]
        self.l_error[idx].remove()
        try:
            for unit in input_block:
                *i_setup, i_expr, l_op = unit
                if i_setup:
                    exec(''.join(ip.value for ip in i_setup))
                op = eval(i_expr.value)
                l_op.update(Pretty(op))
        except ERROR_TYPES as e:
            t = Panel(f'{e}', title=f'{type(e).__name__}', title_align='left')
            self.l_error[idx] = Label(t, classes='error')
            self.v_code_block[idx].mount(self.l_error[idx])
            #self.v_code_block[idx].styles.background = 'ansi_red'

    def load_cheatsheet(self):
        self.v_code_block = []
        self.input_collection = []
        comment_highlighter = CommentHighlighter()
        with open('cheatsheet.json') as f:
            md = iter(json.load(f).values())
        idx = 0
        for info in md:
            code_block = next(md)
            self.v_code_block.append(Vertical(classes='code_container'))
            self.input_collection.append([])
            for unit in code_block:
                lines = unit.splitlines(keepends=True)
                *setup, expr = lines
                if setup:
                    exec(''.join(setup))
                op = eval(expr)

                t = [Input(value=line, classes='code_ip',
                           highlighter=comment_highlighter, name=str(idx))
                     for line in lines]
                l_op = Label(Pretty(op), classes='code_op')
                t.append(l_op)
                self.input_collection[idx].append(t)
                self.v_code_block[idx].mount(*t)
            self.v_cheatsheet.mount(Label(Panel(Markdown(info)), shrink=True))
            self.v_cheatsheet.mount(self.v_code_block[idx])
            idx += 1
        self.l_error = [Label('') for i in range(idx)]


class PyRegexPlayground(App):
    CSS_PATH = 'pyregex_playground.css'
    BINDINGS = [
        Binding('ctrl+u', 'update_ip', 'Update ip', show=True),
        ('ctrl+s,f2', 'push_screen("cheatsheet")', 'Cheatsheet'),
        ('ctrl+g,f1', 'push_screen("help")', 'Help'),
        ('ctrl+t', 'toggle_theme', 'Theme'),
        ('ctrl+q', 'app.quit', 'Quit'),
    ]
    SCREENS = {'help': Help(),
               'cheatsheet': Cheatsheet()}

    def __init__(self):
        super().__init__()

        self.l_compile = Label('Compile', classes='name')
        self.l_action = Label('Action', classes='name')

        self.l_compile_error = Label('')
        self.l_action_error = Label('')

        self.read_data()
        self.l_input = Label(classes='ip_op')
        self.ip_panel = partial(Panel, title='ip', title_align='center')
        self.l_input.update(self.ip_panel(self.data))

        self.l_output = Label(classes='ip_op')
        self.op_panel = partial(Panel, title='Output', title_align='center')
        self.l_output.update(self.op_panel(''))

        placeholder = 'Search pattern. Press Enter to compile.'
        self.i_compile = Input(placeholder=placeholder, value="re.compile(r'')")
        self.i_compile.styles.background = 'lightgray'
        placeholder = "Function to run. Example: pat.sub(r'X', ip)"
        self.i_action = Input(placeholder=placeholder)
        self.i_action.styles.background = 'lightgray'

    def compose(self):
        yield Label('[b]Python re(gex)? playground', classes='header')
        self.v_compile = Vertical(
                Horizontal(self.l_compile, self.i_compile, classes='container'),
                classes='container')
        yield self.v_compile
        yield self.l_input
        self.v_action = Vertical(
                Horizontal(self.l_action, self.i_action, classes='container'),
                classes='container')
        yield self.v_action
        yield self.l_output
        yield Footer()

    def on_mount(self):
        self.dark = False
        self.i_compile.focus()

    async def on_input_submitted(self, event):
        self.l_compile_error.remove()
        ip = self.data
        try:
            self.i_compile.styles.background = 'lightgray'
            pat = eval(self.i_compile.value)
        except ERROR_TYPES as e:
            t = Panel(f'{e}', title=f'{type(e).__name__}', title_align='left')
            self.l_compile_error = Label(t, classes='error')
            self.v_compile.mount(self.l_compile_error)
            self.i_compile.styles.background = 'ansi_red'
        else:
            op = Text(ip)
            for m in pat.finditer(ip):
                op.stylize('bold red', *m.span())
            self.l_input.update(self.ip_panel(op))

        self.l_action_error.remove()
        try:
            self.i_action.styles.background = 'lightgray'
            if self.i_action.value:
                op = eval(self.i_action.value)
            else:
                op = ''
        except ERROR_TYPES as e:
            t = Panel(f'{e}', title=f'{type(e).__name__}', title_align='left')
            self.l_action_error = Label(t, classes='error')
            self.v_action.mount(self.l_action_error)
            self.i_action.styles.background = 'ansi_red'
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

