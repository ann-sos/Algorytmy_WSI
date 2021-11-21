import pytest

"""Min is using O, while Max uses X"""


class Field:


    def __init__(self, value, sign=""):
        self.value = value
        self.sign = sign

    def fill_field(self, sign):
        if sign in ["O", "X"]:
            self.sign = sign
            if self.sign == "O":
                self.value *= -1


class Board:
    def __init__(self, states=None):
        self.board = []
        self.state = 0
        values = [[3, 2, 3], [2, 4, 2], [3, 2, 3]]
        for i in range(3):
            row = []
            for j in range(3):
                row.append(Field(values[i][j]))
            self.board.append(row)
        if states:
            for s_key, s_val in states.items():
                self.board[(s_key - 1) // 3][(s_key - 1) % 3].fill_field(s_val)

    def heuristics(self):
        state = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j].sign != "":
                    state += self.board[i][j].value
        self.state = state
        return state

    def change_state(self, idx, idy, sign):
        if idx in range(3) and idx in range(3) and sign in ["O", "X"]:
            self.board[idx][idy].sign = sign


    def is_board_full(self):
        for row in self.board:
            for item in row:
                if item.sign == "":
                    return False
        return True

    def is_terminal(self, player):
        # check columns
        for i in range(len(self.board)):
            terminal = True
            for j in range(len(self.board)):
                if self.board[j][i].sign is not player:
                    terminal = False
                    break
            if terminal:
                return terminal
        # check rows
        for i in range(len(self.board)):
            terminal = True
            for j in range(len(self.board)):
                if self.board[i][j].sign is not player:
                    terminal = False
                    break
            if terminal:
                return terminal
        # check diagonals
        terminal = True
        for i in range(len(self.board)):
            if self.board[i][i].sign is not player:
                terminal = False
                break
        if terminal:
            return terminal
        # 0,2 1,1, 2,0
        terminal = True
        for i in range(len(self.board)):
            if self.board[i][2-i].sign is not player:
                terminal = False
                break
        if terminal:
            return terminal
        # check if full
        return self.is_board_full()

    def successors(self):

        pass


def alphabeta(state, depth, max_move, alpha, beta):
    if state.is_terminal() or depth == 0:
        return state.heuristics()
    U = state.successors()
    if max_move:
        for u in U:
            alpha = max(alpha, alphabeta(u, depth - 1, alpha, beta))
            if alpha >> beta:
                return beta
        return alpha
    pass


def main():
    cpu1_choice = 'X'
    cpu2_choice = 'O'


def test_field():
    my_field = Field(4)
    assert my_field.value == 4


def test_empty_board():
    empty_board = Board()
    assert empty_board.heuristics() == 0


def test_changing_state():
    my_board = Board()
    my_board.change_state(1, 1, "O")
    assert my_board.heuristics() == 4


def test_filled_board():
    my_board = Board({3: "X", 5: "O", 9: "X"})
    assert my_board.heuristics() == 2

def test_is_full():
    pass

@pytest.mark.parametrize('state, player, is_terminal',
                         [
                             ({1: "O", 2: "O", 5: "O", 9: "X"}, "X", False),
                             ({1: "O", 5: "O", 7: "X", 9: "X"}, "X", False),
                             ({1: "O", 5: "O", 6: "X", 9: "X"}, "X", False),
                             ({1: "X", 4: "X", 7: "X"}, "X", True),     # first column
                             ({1: "X", 5: "X", 9: "X"}, "X", True),     # diagonal
                             ({1: "X", 3: "O", 4: "X", 5: "O", 7: "O", 9: "X"}, "O", True)      # diagonal O
                         ])
def test_terminal_states(state: dict, player, is_terminal):
    assert Board(state).is_terminal(player) == is_terminal
