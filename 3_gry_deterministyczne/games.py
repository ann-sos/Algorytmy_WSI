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
        self.board = {}
        self.state = 0
        values = [3, 2, 3, 2, 4, 2, 3, 2, 3]
        for i in range(9):
            self.board[i+1] = Field(values[i])
        if states:
            for s_key, s_val in states.items():
                self.board[s_key].fill_field(s_val)

    def heuristics(self):
        state = 0
        for i in range(9):
            if self.board[i + 1].sign != "":
                state += self.board[i+1].value
        self.state = state
        return state

    def change_state(self, idx, sign):
        if idx in range(1, 10) and sign in ["O", "X"]:
            self.board[idx].sign = sign


def is_terminal(s):
    pass


def heuristics(s):
    pass


def successors(s):
    return []


def alphabeta(state, depth, max_move, alpha, beta):
    if is_terminal(state) or depth == 0:
        return heuristics(state)
    U = successors(state)
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
    my_board.change_state(5, "O")
    assert my_board.heuristics() == 4


def test_filled_board():
    my_board = Board({3: "X", 5: "O", 9: "X"})
    assert my_board.heuristics() == 2
