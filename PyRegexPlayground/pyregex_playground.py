from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Label, Input, MarkdownViewer, Button
from textual.screen import Screen
from rich.panel import Panel
from rich.text import Text
from rich.pretty import Pretty
from rich.highlighter import Highlighter
from rich.markdown import Markdown as RichMarkdown

import json
import re
from functools import partial
from math import factorial
import os
from pathlib import Path

ERROR_TYPES = (re.error, SyntaxError, TypeError, ValueError,
               NameError, AttributeError, IndexError)

class CommentHighlighter(Highlighter):
    def highlight(self, text):
        if str(text[0]) == '#':
            text.stylize('italic color(8)')


class ShowMarkdown(Screen):
    BINDINGS = [Binding('escape', 'app.pop_screen', 'Go back'),
                Binding('ctrl+n', 'navigation', 'Navigation'),
               ]

    def __init__(self, md_file):
        super().__init__()
        self.md_file = md_file
        self.v_container = Vertical()

    def compose(self):
        yield self.v_container
        yield Footer()

    def on_mount(self):
        with open(self.md_file, encoding='UTF-8') as f:
            md = f.read()
        self.m_view = MarkdownViewer(md, show_table_of_contents=False)
        self.v_container.mount(self.m_view)

    def action_navigation(self):
        self.m_view.show_table_of_contents ^= True


class Examples(Screen):
    BINDINGS = [Binding('escape', 'app.pop_screen', 'Go back'),
                Binding('ctrl+r', 'reload', 'Reload'),
                Binding('up', 'focus_previous', 'Focus previous', show=False),
                Binding('down', 'focus_next', 'Focus next', show=False),
               ]

    def compose(self):
        yield Label('[b]Interactive Examples', classes='header')
        self.v_container = Vertical(classes='container')
        yield self.v_container
        yield Footer()

    def on_mount(self):
        self.load_examples()

    def on_input_submitted(self, event):
        idx = int(event.input.name)
        input_block = self.input_collection[idx]
        for unit in input_block:
            *i_setup, i_expr, l_op = unit
            try:
                if i_setup:
                    exec(''.join(ip.value for ip in i_setup))
                op = eval(i_expr.value)
                l_op.update(Pretty(op))
            except ERROR_TYPES as e:
                t = Panel(f'{e}', title=f'{type(e).__name__}', title_align='left')
                l_op.update(t)
                l_op.styles.color = 'red'

    def load_examples(self):
        self.v_examples = Vertical(classes='container')
        self.v_code_block = []
        self.input_collection = []
        comment_highlighter = CommentHighlighter()
        with open('examples.json', encoding='UTF-8') as f:
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

                t = [Input(value=line, classes='examples_ip',
                           highlighter=comment_highlighter, name=str(idx))
                     for line in lines]
                l_op = Label(Pretty(op), classes='examples_op')
                t.append(l_op)
                self.input_collection[idx].append(t)
                self.v_code_block[idx].mount(*t)
            self.v_examples.mount(Label(RichMarkdown(info), classes='examples_md'))
            self.v_examples.mount(self.v_code_block[idx])
            idx += 1
        self.v_container.mount(self.v_examples)

    def action_reload(self):
        self.v_examples.remove()
        self.load_examples()


class Playground(Screen):
    BINDINGS = [Binding('ctrl+p', 'update_ip', 'Update ip', show=True),
                Binding('f1', 'guide', 'App Guide', show=False),
                Binding('f2', 'cheatsheet', 'Cheatsheet', show=False),
                Binding('f3', 'examples', 'Interactive Examples', show=False),
                ('up', 'focus_previous', 'Focus previous'),
                ('down', 'focus_next', 'Focus next'),
               ]

    def __init__(self):
        super().__init__()

        self.l_compile = Label('Compile', classes='playground_name')
        self.l_action = Label('Action', classes='playground_name')

        self.l_compile_error = Label('')
        self.l_action_error = Label('')

        os.chdir(Path(__file__).parent.resolve())
        self.ip_file = 'ip.txt'
        self.read_data()
        self.l_input = Label(classes='playground_ip_op')
        self.ip_panel = partial(Panel, title='ip', title_align='center')
        self.l_input.update(self.ip_panel(self.data))

        self.l_output = Label(classes='playground_ip_op')
        self.op_panel = partial(Panel, title='Output', title_align='center')
        self.l_output.update(self.op_panel(''))

        self.code_bg_color = 'silver'
        self.error_color = 'ansi_red'

        placeholder = 'Search pattern. Press Enter to compile.'
        self.i_compile = Input(placeholder=placeholder, value="re.compile(r'')",
                               classes='playground_ip')
        self.i_compile.styles.background = self.code_bg_color
        placeholder = "Function to run. Example: pat.sub('X', ip)"
        self.i_action = Input(placeholder=placeholder,
                              classes='playground_ip')
        self.i_action.styles.background = self.code_bg_color

        self.b_guide = Button('App Guide', classes='buttons')
        self.b_cheatsheet = Button('Cheatsheet', classes='buttons',
                                   variant="success")
        self.b_examples = Button('Interactive Examples', classes='buttons')

    def compose(self):
        yield Label('[b]Python re(gex)? playground', classes='header')
        with Vertical(classes='code_container') as self.v_compile:
            yield Horizontal(self.l_compile, self.i_compile, classes='container')
        yield self.l_input
        with Vertical(classes='code_container') as self.v_action:
            yield Horizontal(self.l_action, self.i_action, classes='container')
        yield self.l_output
        with Horizontal(classes='container'):
            yield self.b_guide
            yield self.b_cheatsheet
            yield self.b_examples
        yield Footer()

    def on_mount(self):
        self.i_compile.focus()

    def on_input_submitted(self, event):
        self.l_compile_error.remove()
        ip = self.data
        try:
            self.i_compile.styles.background = self.code_bg_color
            pat = eval(self.i_compile.value)
        except ERROR_TYPES as e:
            t = Panel(f'{e}', title=f'{type(e).__name__}', title_align='left')
            self.l_compile_error = Label(t, classes='playground_error')
            self.v_compile.mount(self.l_compile_error)
            self.i_compile.styles.background = self.error_color
        else:
            op = Text(ip)
            for m in pat.finditer(ip):
                op.stylize('bold red', *m.span())
            self.l_input.update(self.ip_panel(op))

        self.l_action_error.remove()
        try:
            self.i_action.styles.background = self.code_bg_color
            if self.i_action.value:
                op = eval(self.i_action.value)
            else:
                op = ''
        except ERROR_TYPES as e:
            t = Panel(f'{e}', title=f'{type(e).__name__}', title_align='left')
            self.l_action_error = Label(t, classes='playground_error')
            self.v_action.mount(self.l_action_error)
            self.i_action.styles.background = self.error_color
        else:
            if type(op) != str:
                op = Pretty(op)
            self.l_output.update(self.op_panel(op))

    def on_button_pressed(self, event):
        button_label = str(event.button.label)
        if button_label == 'Cheatsheet':
            self.action_cheatsheet()
        elif button_label == 'Interactive Examples':
            self.action_examples()
        elif button_label == 'App Guide':
            self.action_guide()

    def read_data(self):
        with open(self.ip_file, encoding='UTF-8') as f:
            self.data = f.read()

    def action_guide(self):
        self.app.push_screen('guide')

    def action_cheatsheet(self):
        self.app.push_screen('cheatsheet')

    def action_examples(self):
        self.app.push_screen('examples')

    def action_update_ip(self):
        self.read_data()
        self.l_input.update(self.ip_panel(self.data))

class PyRegexPlayground(App):
    SCREENS = {'playground': Playground(),
               'guide': ShowMarkdown('app_guide.md'),
               'cheatsheet': ShowMarkdown('cheatsheet.md'),
               'examples': Examples()}
    CSS_PATH = 'pyregex_playground.css'
    BINDINGS = [('ctrl+t', 'toggle_theme', 'Theme'),
                ('ctrl+q', 'app.quit', 'Quit')]

    def on_mount(self):
        self.app.dark = False
        self.app.push_screen('playground')

    def action_toggle_theme(self):
        self.app.dark ^= True

def main():
    os.chdir(Path(__file__).parent.resolve())
    app = PyRegexPlayground()
    app.run()

if __name__ == '__main__':
    main()

