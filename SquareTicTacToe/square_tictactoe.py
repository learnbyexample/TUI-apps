from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Label
from typing import List
import random

class SquareTicTacToeApp(App):
    """Square Tic Tac Toe game."""

    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "square_tictactoe.css"
    BINDINGS = [
        ("d", "toggle_theme", "Toggle theme"),
        Binding("q", "app.quit", "Quit", show=True),
    ]

    def __init__(self) -> None:
        super().__init__()

        self.active = "ACTIVE"
        self.state = "INACTIVE"
        self.corners = 4
        self.total_cells = 16
        self.easy, self.hard = (0, 1)
        self.difficulty = self.easy
        self.ai = {"value": 1, "char": "✖️ ", "win": "AI WINS",
                   "variant": "warning", "variant_win": "error"}
        self.user = {"value": self.corners+1, "char": "⭕️", "win": "USER WINS",
                     "variant": "primary", "variant_win": "success"}
        self.max_ai_sum = (self.corners-1) * self.ai["value"] # type: ignore
        self.max_user_sum = (self.corners-1) * self.user["value"] # type: ignore
        self.all_squares = ((0, 1, 4, 5), (1, 2, 5, 6), (2, 3, 6, 7),
                            (4, 5, 8, 9), (5, 6, 9, 10), (6, 7, 10, 11),
                            (8, 9, 12, 13), (9, 10, 13, 14), (10, 11, 14, 15),
                            (0, 2, 8, 10), (1, 3, 9, 11), (4, 6, 12, 14),
                            (5, 7, 13, 15), (0, 3, 12, 15), (1, 4, 6, 9),
                            (2, 5, 7, 10), (5, 8, 10, 13), (6, 9, 11, 14),
                            (1, 7, 8, 14), (2, 4, 11, 13))

        self.status = Label(self.state, id="info")
        self.status.border_title = 'Game Status'
        self.new_game = Button(label="New Game", id="new_game")
        self.choice = (Button(label="Easy", id="easy", variant="success"),
                       Button(label="Hard", id="hard", variant="default"))
        self.cell_buttons = tuple(Button(label="", name=str(n),
                                         classes="cell", disabled=True)
                                  for n in range(self.total_cells))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        title = ("[b]Square Tic Tac Toe[/b]\n"
                 "Like Tic Tac Toe, but form a square "
                 "with 4 corners instead of a line.")
        yield Label(renderable=title, id="header")
        yield Container(
                self.status,
                Container(*self.cell_buttons, id="board"),
                Container(self.new_game, *self.choice, id="control"))
        yield Footer()

    def on_mount(self) -> None:
        """Set up the application on startup."""

        self.dark = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when any button is pressed."""

        button_id = event.button.id
        if button_id == "new_game":
            self.start_new_game()
        elif button_id == "easy":
            self.choice[0].variant = "success"
            self.choice[1].variant = "default"
        elif button_id == "hard":
            self.choice[0].variant = "default"
            self.choice[1].variant = "error"
        else:
            cell_idx = int(event.button.name) # type: ignore
            if self.state == self.active and cell_idx in self.available_moves:
                self.update_cell(self.user, cell_idx)
                self.ai_response()

    def start_new_game(self) -> None:
        """Initialize stuff on starting a new game."""

        for button in self.cell_buttons:
            button.label = ""
            button.variant = "default"
            button.disabled = False
        self.board = [0] * self.total_cells
        self.available_moves = list(range(self.total_cells))
        self.ai["last_move"] = 0
        self.user["last_move"] = 0
        self.state = self.active
        self.status.update(self.state)
        if self.choice[0].variant == "success":
            self.difficulty = self.easy
        else:
            self.difficulty = self.hard
        if self.difficulty == self.hard or random.randrange(2):
            self.ai_response()

    def update_cell(self, player: dict, move: int) -> None:
        """Update board cells for user and ai moves."""

        self.cell_buttons[player["last_move"]].variant = "default"
        player["last_move"] = move
        self.board[move] = player["value"]
        self.cell_buttons[move].label = player["char"]
        self.cell_buttons[move].variant = player["variant"]
        self.available_moves.remove(move)
        self.check_win_tie(player)

    def check_win_tie(self, player: dict) -> None:
        """Check if either player has won or if the game is tied."""

        winner_sum = self.corners * player["value"]
        self.winning_squares = []
        for square in self.all_squares:
            if sum(self.board[i] for i in square) == winner_sum:
                self.state = player["win"]
                self.winning_squares.append(square)
                self.highlight_winning_squares(player)
                break # implies that only the first winning square is highlighted
        else:
            if self.state == self.active and not self.available_moves:
                self.state = "TIE"
        self.status.update(self.state)

    def ai_response(self) -> None:
        """Move made by AI based on Easy/Hard modes."""

        if self.state == self.active and self.available_moves:
            if self.difficulty == self.easy:
                move = random.choice(self.available_moves)
            else:
                move = self.ai_hard_move()
            self.update_cell(self.ai, move)

    def ai_hard_move(self) -> int:
        """Returns move for AI hard mode."""

        self.update_weights()

        # making a winning move or block a winning move
        if self.ai_winning_indexes:
            return random.choice(self.ai_winning_indexes)
        elif self.user_winning_indexes:
            return random.choice(self.user_winning_indexes)

        # if there are no possible squares left, return a random move
        max_user_weight = max(self.user_weights)
        max_ai_weight = max(self.ai_weights)
        if max_user_weight == 0 and max_ai_weight == 0:
            return random.choice(self.available_moves)

        # there can be multiple indexes with max weight
        def max_moves(seq, val):
            return [i for i,w in enumerate(seq) if w == val]
        max_user_moves = max_moves(self.user_weights, max_user_weight)
        max_ai_moves = max_moves(self.ai_weights, max_ai_weight)

        # randomize multiple indexes and choose best move based on weights
        if max_user_weight > max_ai_weight:
            random.shuffle(max_user_moves)
            return max(max_user_moves, key=lambda x: self.ai_weights[x])
        else:
            random.shuffle(max_ai_moves)
            return max(max_ai_moves, key=lambda x: self.user_weights[x])

    def update_weights(self) -> None:
        """AI logic to assign weights."""

        def update(s, w, t, ot) -> None:
            for i in square:
                if self.board[i] == 0:
                    w[i] += t * t + 1
                    if ot == self.max_ai_sum:
                        self.ai_winning_indexes.append(i)
                    elif ot == self.max_user_sum:
                        self.user_winning_indexes.append(i)

        self.user_weights = [0] * self.total_cells
        self.ai_weights = [0] * self.total_cells
        self.user_winning_indexes: List[int] = []
        self.ai_winning_indexes: List[int] = []
        for square in self.all_squares:
            total = sum(self.board[i] for i in square)
            if total == 0:
                update(square, self.user_weights, 0, 0)
                update(square, self.ai_weights, 0, 0)
            elif total <= self.max_ai_sum:
                update(square, self.ai_weights, total, total)
            else:
                q, r = divmod(total, self.user['value']) # type: ignore
                if r == 0:
                    update(square, self.user_weights, q, total)

    def highlight_winning_squares(self, player: dict) -> None:
        """Set all cell variants to default and highlight winning square."""

        for button in self.cell_buttons:
            button.variant = "default"
        for square in self.winning_squares:
            for i in square:
                self.cell_buttons[i].variant = player["variant_win"]

    def action_toggle_theme(self) -> None:
        """An action to toggle theme."""

        self.dark = not self.dark

def main():
    app = SquareTicTacToeApp()
    app.run()

if __name__ == "__main__":
    main()

