from textual.app import App
from textual.binding import Binding
from textual.containers import Grid
from textual.widgets import Button, Footer, Label
from textual.widgets import RadioButton, RadioSet
import random

class ConnectFourApp(App):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = 'connect_four.css'
    BINDINGS = [
                Binding('n', 'new_game', 'New Game'),
                Binding('t', 'toggle_theme', 'Toggle theme'),
                Binding('q', 'app.quit', 'Quit'),
               ]

    def __init__(self):
        super().__init__()

        self.active = 'GAME IN PROGRESS'
        self.state = 'PRESS n TO START A NEW GAME'
        self.line_size = 4
        self.rows = 6
        self.columns = 7
        self.total_cells = self.rows * self.columns
        self.generate_winning_moves()

        self.easy, self.medium, self.hard = (0, 1, 2)
        self.difficulty = self.easy
        self.four, self.square, self.both = (0, 1, 2)
        self.game_type = self.four
        self.user_first, self.ai_first = (0, 1)
        self.first_move = self.user_first
        
        self.ai = {'value': 1, 'char': '✖️ ', 'win': 'AI WINS',
                   'variant': 'warning', 'variant_win': 'error'}
        self.user = {'value': self.line_size+1, 'char': '⭕️', 'win': 'USER WINS',
                     'variant': 'primary', 'variant_win': 'success'}
        self.max_ai_sum = (self.line_size-1) * self.ai['value']
        self.max_user_sum = (self.line_size-1) * self.user['value']

        self.status = Label(self.state, id='info')
        self.rb_choice = (RadioButton('Easy'), RadioButton('Medium'),
                          RadioButton('Hard'))
        self.rb_choice[self.difficulty].value = True
        self.rb_first_move = (RadioButton('User first'), RadioButton('AI first'))
        self.rb_first_move[self.first_move].value = True
        self.rb_game_type = (RadioButton('Connect Four'),
                             RadioButton('Connect Square'), RadioButton('Both'))
        self.rb_game_type[self.game_type].value = True

        self.cell_buttons = tuple(Button(label='', name=str(n),
                                         classes='cell', disabled=True)
                                  for n in range(self.total_cells))
        self.grid = Grid(*self.cell_buttons, id='board')
        self.grid.styles.grid_size_rows = self.rows
        self.grid.styles.grid_size_columns = self.columns
        self.grid.styles.grid_rows = '3'
        self.grid.styles.grid_columns = '6'
        self.grid.styles.grid_gutter_vertical = 0
        self.grid.styles.grid_gutter_horizontal = 0    

    def generate_winning_moves(self):
        self.all_lines = []
        for i in range(self.rows):
            for j in range(self.columns-self.line_size+1):
                n = i * self.columns + j
                self.all_lines.append((n, n+1, n+2, n+3))
        for i in range(self.rows-self.line_size+1):
            for j in range(self.columns):
                n0 = (i+0) * self.columns + j
                n1 = (i+1) * self.columns + j
                n2 = (i+2) * self.columns + j
                n3 = (i+3) * self.columns + j
                self.all_lines.append((n0, n1, n2, n3))
        for i in range(self.rows-self.line_size+1):
            for j in range(self.columns-self.line_size+1):
                n0 = (i+0) * self.columns + (j+0)
                n1 = (i+1) * self.columns + (j+1)
                n2 = (i+2) * self.columns + (j+2)
                n3 = (i+3) * self.columns + (j+3)
                self.all_lines.append((n0, n1, n2, n3))
                n0 = (i+0) * self.columns + (j+3)
                n1 = (i+1) * self.columns + (j+2)
                n2 = (i+2) * self.columns + (j+1)
                n3 = (i+3) * self.columns + (j+0)
                self.all_lines.append((n0, n1, n2, n3))

        self.all_squares = []
        t = self.total_cells
        for i in range(self.rows-1):
            for j in range(self.columns-1):
                for k in range(1, self.columns):
                    n0 = (i+0) * self.columns + (j+0)
                    n1 = (i+0) * self.columns + (j+k)
                    n2 = (i+k) * self.columns + (j+0)
                    n3 = (i+k) * self.columns + (j+k)
                    if n0 >= t or n1 >= t or n2 >= t or n3 >= t:
                        continue
                    if n1 >= (i*self.columns + self.columns):
                        continue
                    self.all_squares.append((n0, n1, n2, n3))

        for i in range(self.rows-2):
            for j in range(self.columns-2):
                for k in range(1, self.rows//2):
                    n0 = (i+0)   * self.columns + (j+k)
                    n1 = (i+k)   * self.columns + (j+0)
                    n2 = (i+k)   * self.columns + (j+2*k)
                    n3 = (i+2*k) * self.columns + (j+k)
                    if n0 >= t or n1 >= t or n2 >= t or n3 >= t:
                        continue
                    if n2 >= ((i+k)*self.columns + self.columns):
                        continue
                    self.all_squares.append((n0, n1, n2, n3))

        for i in range(self.rows-3):
            for j in range(self.columns-3):
                for k in range(2, self.rows//2 + 1):
                    for l in range(self.columns-4):
                        n0 = (i+0)       * self.columns + (j+k+l)
                        n1 = (i+k-1)     * self.columns + (j+0)
                        n2 = (i+k+l)     * self.columns + (j+2*k-1+l)
                        n3 = (i+2*k-1+l) * self.columns + (j+k-1)
                        if n0 >= t or n1 >= t or n2 >= t or n3 >= t:
                            continue
                        if n2 >= ((i+k+l)*self.columns + self.columns):
                            continue
                        self.all_squares.append((n0, n1, n2, n3))
                        n0 = (i+0)       * self.columns + (j+k-1)
                        n1 = (i+k-1)     * self.columns + (j+2*k-1+l)
                        n2 = (i+k+l)     * self.columns + (j+0)
                        n3 = (i+2*k-1+l) * self.columns + (j+k+l)
                        self.all_squares.append((n0, n1, n2, n3))

    def compose(self):
        yield Label(renderable='[b]Connect Four[/b]', id='header')
        yield self.grid
        yield self.status
        with RadioSet(name='choice', classes='radio'):
            for rb in self.rb_choice:
                yield rb        
        with RadioSet(name='first_move', classes='radio'):
            for rb in self.rb_first_move:
                yield rb        
        with RadioSet(name='game_type', classes='radio'):
            for rb in self.rb_game_type:
                yield rb        
        yield Footer()

    def on_mount(self):
        self.dark = False

    def on_button_pressed(self, event):
        cell_idx = int(event.button.name)
        if self.state == self.active and cell_idx in self.available_moves:
            self.update_cell(self.user, cell_idx)
            self.ai_response()

    def update_available_moves(self):
        for i in range(self.rows-1):
            for j in range(self.columns):
                n1 = i*self.columns + j
                n2 = (i+1)*self.columns + j
                if self.board[n1] == 0 and self.board[n2] != 0:
                    self.available_moves.add(n1)
    
    def start_new_game(self):
        if self.game_type == self.four:
            self.all_winning_moves = self.all_lines
        elif self.game_type == self.square:
            self.all_winning_moves = self.all_squares
        else:
            self.all_winning_moves = self.all_lines + self.all_squares

        for button in self.cell_buttons:
            button.label = ''
            button.variant = 'default'
            button.disabled = False
        self.board = [0] * self.total_cells
        self.available_moves = set()
        for j in range(self.columns):
            self.available_moves.add((self.rows-1)*self.columns + j)
        self.ai['last_move'] = 0
        self.user['last_move'] = 0
        self.state = self.active
        self.status.update(self.state)
        if self.first_move == self.ai_first:
            self.ai_response()

    def on_radio_set_changed(self, event):
        idx = event.radio_set.pressed_index
        if event.radio_set.name == 'choice':
            self.difficulty = idx
        elif event.radio_set.name == 'first_move':
            self.first_move = idx
        else:
            self.game_type = idx

    def update_cell(self, player, move):
        self.cell_buttons[player['last_move']].variant = 'default'
        player['last_move'] = move
        self.board[move] = player['value']
        self.cell_buttons[move].label = player['char']
        self.cell_buttons[move].variant = player['variant']
        self.available_moves.remove(move)
        self.update_available_moves()
        self.check_win_tie(player)

    def check_win_tie(self, player):
        winner_sum = self.line_size * player['value']
        self.winning_lines = []
        for line in self.all_winning_moves:
            if sum(self.board[i] for i in line) == winner_sum:
                self.state = player['win']
                self.winning_lines.append(line)
                self.highlight_winning_lines(player)
                break # implies that only the first winning line is highlighted
        else:
            if self.state == self.active and not self.available_moves:
                self.state = 'TIE'
        self.status.update(self.state)

    def highlight_winning_lines(self, player):
        for button in self.cell_buttons:
            button.variant = 'default'
        for line in self.winning_lines:
            for i in line:
                self.cell_buttons[i].variant = player['variant_win']

    def ai_response(self):
        if self.state == self.active and self.available_moves:
            if self.difficulty == self.easy:
                move = random.choice(tuple(self.available_moves))
            else:
                move = self.choose_ai_move()
            self.update_cell(self.ai, move)

    def choose_ai_move(self):
        self.update_weights()

        # making a winning move or block a winning move
        if self.ai_winning_indexes:
            return random.choice(self.ai_winning_indexes)
        elif self.user_winning_indexes:
            return random.choice(self.user_winning_indexes)

        max_user_weight = max_ai_weight = 0
        if self.user_weights:
            max_user_weight = max(self.user_weights.values())
        if self.ai_weights:
            max_ai_weight = max(self.ai_weights.values())

        # block user's best move
        if self.difficulty == self.hard and max_user_weight > max_ai_weight:
            return max((k for k,v in self.user_weights.items()
                        if v == max_user_weight),
                       key=lambda x: self.ai_weights.get(x, 0))

        # if there are no possible lines left, return a random move
        if max_ai_weight == 0:
            return random.choice(tuple(self.available_moves))

        # play ai's best move
        if self.difficulty == self.hard:
            return max((k for k,v in self.ai_weights.items()
                        if v == max_ai_weight),
                       key=lambda x: self.user_weights.get(x, 0))
        else:
            return random.choice(sorted(self.ai_weights,
                                        key=lambda x: self.ai_weights[x]))

    def update_weights(self):
        def update(w, t, ot):
            for i in line:
                if self.board[i] == 0:
                    if i in self.available_moves:
                        w[i] = w.get(i, 0) + (t * t + 1) * (1 + (i // self.columns))
                        if ot == self.max_ai_sum:
                            self.ai_winning_indexes.append(i)
                        elif ot == self.max_user_sum:
                            self.user_winning_indexes.append(i)
                    elif ot == self.max_user_sum:
                        self.shifted_user_winning_indexes.append(i + self.columns)

        self.user_weights = {}
        self.ai_weights = {}
        self.user_winning_indexes = []
        self.shifted_user_winning_indexes = []
        self.ai_winning_indexes = []
        for line in self.all_winning_moves:
            total = sum(self.board[i] for i in line)
            if total == 0:
                update(self.user_weights, 0, 0)
                update(self.ai_weights, 0, 0)
            elif total <= self.max_ai_sum:
                update(self.ai_weights, total, total)
            else:
                q, r = divmod(total, self.user['value'])
                if r == 0:
                    update(self.user_weights, q, total)

        for i in self.shifted_user_winning_indexes:
            if i in self.user_weights:
                del self.user_weights[i]
            if self.difficulty == self.hard and i in self.ai_weights:
                del self.ai_weights[i]

    def action_new_game(self):
        self.start_new_game()

    def action_toggle_theme(self):
        self.dark = not self.dark

def main():
    app = ConnectFourApp()
    app.run()

if __name__ == '__main__':
    main()

