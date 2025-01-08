from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Footer, Label, Input, Button, TextArea
from textual.widgets import MarkdownViewer, ContentSwitcher
from rich.text import Text
from rich.pretty import Pretty
from rich.highlighter import Highlighter

import json
import os
import re
from math import factorial
from pathlib import Path

ERROR_TYPES = (re.error, SyntaxError, TypeError, ValueError,
               NameError, AttributeError, IndexError)

class CommentHighlighter(Highlighter):
    def highlight(self, text):
        if str(text[0]) == '#':
            text.stylize('italic color(8)')

class PyRegexPlayground(App):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = 'pyregex_playground.css'
    BINDINGS = [
        Binding('f1', 'app_guide', 'App Guide', show=False),
        Binding('f2', 'playground', 'Regex Playground', show=False),
        Binding('f3', 'cheatsheet', 'Cheatsheet', show=False),
        Binding('f4', 'examples', 'Interactive Examples', show=False),
        Binding('ctrl+p', 'update_ip', 'Update ip'),
        Binding('ctrl+r', 'run', 'Run'),
        Binding('ctrl+z', 'discard', 'Discard changes'),
        Binding('ctrl+t', 'toggle_theme', 'Theme'),
        Binding('ctrl+q', 'app.quit', 'Quit'),
    ]

    def __init__(self):
        super().__init__()

        self.data = Path.read_text(
                        Path('ip.txt'), encoding='UTF-8').removesuffix('\n')

        self.t_input = TextArea(id='ip_edit', soft_wrap=False)
        self.t_input.border_title = 'Edit ip'
        self.t_input.indent_width = 8
        self.l_input = Label(classes='playground_ip_op', markup=False, id='ip_label')
        self.l_input.border_title = 'ip'
        self.l_input.update(self.data)
        self.t_input.text = self.data

        self.l_output = Label(classes='playground_ip_op', markup=False)
        self.l_output.border_title = 'Output'

        self.code_bg_color = 'lightgray'
        self.error_color = 'ansi_red'
        self.l_compile_error = Label()
        self.l_action_error = Label()

        placeholder = 'Search pattern. Press Enter to compile.'
        self.i_compile = Input(placeholder=placeholder, value="re.compile(r'')",
                               classes='playground_ip')
        self.i_compile.styles.background = self.code_bg_color
        placeholder = "Function to run. For example: pat.sub('X', ip)"
        self.i_action = Input(placeholder=placeholder,
                              classes='playground_ip')
        self.i_action.styles.background = self.code_bg_color

        self.v_container = VerticalScroll(classes='container')

        with open('app_guide.md', encoding='UTF-8') as f:
            self.m_guide = MarkdownViewer(f.read(), show_table_of_contents=False)

        with open('cheatsheet.md', encoding='UTF-8') as f:
            self.m_cheatsheet = MarkdownViewer(f.read(), show_table_of_contents=False)

        self.b_tabs = (Button('App Guide', name='guide', classes='buttons'),
                       Button('Regex Playground', name='playground',
                              classes='buttons', variant='warning'),
                       Button('Cheatsheet', name='cheatsheet', classes='buttons'),
                       Button('Interactive Examples', name='examples',
                              classes='buttons'))
        self.b_tabs[1].styles.width = '1.5fr'
        self.b_tabs[3].styles.width = '1.5fr'
        for b in self.b_tabs:
            b.can_focus = False

    def compose(self):
        with Horizontal(classes='container'):
            for button in self.b_tabs:
                yield button
        with ContentSwitcher(initial='playground', id='cs_main') as self.cs_tabs:  
            with VerticalScroll(id='playground') as self.v_exercises:
                with Vertical(classes='code_container') as self.v_compile:
                    yield self.i_compile
                with ContentSwitcher(initial='ip_label') as self.cs_input:  
                    yield self.l_input
                    yield self.t_input
                with Vertical(classes='code_container') as self.v_action:
                    yield self.i_action
                yield self.l_output
            with Vertical(id='guide'):
                yield self.m_guide
            with Vertical(id='cheatsheet'):
                yield self.m_cheatsheet
            with VerticalScroll(id='examples'):
                yield self.v_container
        yield Footer()

    def on_mount(self):
        self.dark = False
        self.v_compile.border_title = 'Compile'
        self.v_action.border_title = 'Action'
        self.i_compile.cursor_position = 13
        self.i_compile.focus()
        self.load_examples()

    def on_input_submitted(self, event):
        if self.cs_tabs.current == 'playground':
            self.action_run()
        else:
            self.process_examples(event)

    def process_playground(self):
        self.l_compile_error.remove()
        ip = self.data
        try:
            self.i_compile.styles.background = self.code_bg_color
            pat = eval(self.i_compile.value)
        except ERROR_TYPES as e:
            self.l_compile_error = Label(str(e), classes='error', markup=False)
            self.l_compile_error.border_title = str(type(e).__name__)
            self.v_compile.mount(self.l_compile_error)
            self.i_compile.styles.background = self.error_color
        else:
            op = Text(ip)
            for m in pat.finditer(ip):
                op.stylize('bold red', *m.span())
            self.l_input.update(op)

        self.l_action_error.remove()
        try:
            self.i_action.styles.background = self.code_bg_color
            if self.i_action.value:
                op = eval(self.i_action.value)
            else:
                op = ''
        except ERROR_TYPES as e:
            self.l_action_error = Label(str(e), classes='error', markup=False)
            self.l_action_error.border_title = str(type(e).__name__)
            self.v_action.mount(self.l_action_error)
            self.i_action.styles.background = self.error_color
        else:
            if type(op) != str:
                op = Pretty(op)
            self.l_output.update(op)

    def process_examples(self, event):
        idx = int(event.input.name)
        input_block = self.input_collection[idx]
        for unit in input_block:
            *i_setup, i_expr, l_op = unit
            try:
                if i_setup:
                    exec(''.join(ip.value for ip in i_setup))
                op = eval(i_expr.value)
                l_op.update(Pretty(op))
                l_op.styles.border = ('none', 'red')
                l_op.styles.color = 'black'
            except ERROR_TYPES as e:
                l_op.update(str(e))
                l_op.styles.border = ('round', 'red')
                l_op.styles.color = 'red'
                l_op.border_title = str(type(e).__name__)

    def load_examples(self):
        self.v_code_block = []
        self.input_collection = []
        comment_highlighter = CommentHighlighter()
        with open('examples.json', encoding='UTF-8') as f:
            md = iter(json.load(f).values())
        idx = 0
        md_cb_widgets = []
        for info in md:
            code_block = next(md)
            self.input_collection.append([])
            cb_widgets = []
            for unit in code_block:
                lines = unit.splitlines(keepends=True)
                *setup, expr = lines
                if setup:
                    exec(''.join(setup))
                op = eval(expr)

                t = []
                for line in lines:
                    i = Input(value=line.removesuffix('\n'), classes='examples_ip',
                            highlighter=comment_highlighter, name=str(idx))
                    if line.startswith('#'):
                        i.can_focus = False
                    t.append(i)
                l_op = Label(Pretty(op), classes='examples_op', markup=False)
                t.append(l_op)
                self.input_collection[idx].append(t)
                cb_widgets.extend(t)
            self.v_code_block.append(Vertical(*cb_widgets, classes='code_container'))
            md_cb_widgets.append(Label(info, classes='examples_md'))
            md_cb_widgets.append(self.v_code_block[idx])
            idx += 1
        self.v_examples = Vertical(*md_cb_widgets, classes='container')
        self.v_container.mount(self.v_examples)

    def action_discard(self):
        self.v_examples.remove()
        self.load_examples()

    def action_update_ip(self):
        self.cs_input.current = 'ip_edit'
        self.t_input.focus(scroll_visible=False)

    def action_run(self):
        self.cs_input.current = 'ip_label'
        self.data = self.t_input.text
        self.process_playground()

    def on_button_pressed(self, event):
        self.refresh_bindings()
        name = event.button.name
        self.cs_tabs.current = name
        for b in self.b_tabs:
            b.variant = 'default'
        if name == 'guide':
            idx = 0
        elif name == 'playground':
            idx = 1
        elif name == 'cheatsheet':
            idx = 2
        else:
            idx = 3
        self.b_tabs[idx].variant = 'warning'

    def check_action(self, action, parameters):
        tab = self.cs_tabs.current
        if action in ('update_ip', 'run') and tab != 'playground':
            return False
        if action == 'discard' and tab != 'examples':
            return False
        return True

    def action_app_guide(self):
        self.b_tabs[0].press()

    def action_playground(self):
        self.b_tabs[1].press()

    def action_cheatsheet(self):
        self.b_tabs[2].press()

    def action_examples(self):
        self.b_tabs[3].press()

    def action_toggle_theme(self):
        self.dark = not self.dark

def main():
    os.chdir(Path(__file__).parent.resolve())
    app = PyRegexPlayground()
    app.run()

if __name__ == '__main__':
    main()

