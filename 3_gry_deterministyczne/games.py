import pytest
from random import choice
import copy
"""Min is using O, while Max uses X"""


class Counter:
    calls_count = {1: 0, -1: 0}

    @classmethod
    def increase_count(cls, player):
        cls.calls_count[player] += 1

    @classmethod
    def reset_count(cls):
        cls.calls_count[1] = 0
        cls.calls_count[-1] = 0

    @classmethod
    def return_count(cls):
        return cls.calls_count

class Field:

    def __init__(self, value, sign=""):
        self.value = value
        self.sign = sign

    def fill_field(self, sign):
        if sign in [-1, 1]:
            self.sign = sign
            if self.sign == -1:
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

    def print_board(self):
        for row in self.board:
            for item in row:
                print(item.sign, end="|\t")
            print("\n")

    def change_state(self, idx, idy, sign):
        if idx in range(3) and idx in range(3) and sign in [-1, 1]:
            self.board[idx][idy].sign = sign

    def board_state(self):
        state = {}
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j].sign != "":
                    state[i * 3 + j + 1] = self.board[i][j].sign
        return state

    def is_board_full(self):
        for row in self.board:
            for item in row:
                if item.sign == "":
                    return False
        return True

    def player_won(self, player):
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
            if self.board[i][2 - i].sign is not player:
                terminal = False
                break
        if terminal:
            return terminal

    def is_terminal(self, player):
        if self.player_won(player):
            return True
        # check if full
        return self.is_board_full()

    def list_available(self):
        available = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j].sign == "":
                    available.append(i * 3 + j + 1)
        return available

    def successors(self, player):

        # create a list of available fields
        available = self.list_available()
        # generate successors
        successors = []

        for a in available:
            board_copy = self.board_state()
            board_copy[a] = player
            successors.append(board_copy)
        return successors


def alpha_beta(state, depth, player, alpha, beta):
    Counter.increase_count(player)
    if state.is_terminal(player) or depth == 0:
        return state.heuristics()
    U = state.successors(player)
    if player == 1:
        for u in U:
            alpha = max((alpha, alpha_beta(Board(u), depth - 1, -player, alpha, beta)))
            if alpha <= beta:
                return alpha
        return alpha
    else:
        for u in U:
            beta = min((beta, alpha_beta(Board(u), depth - 1, -player, alpha, beta)))
            if alpha <= beta:
                return beta
        return beta
    pass


def min_max(state: Board, depth, player, a=None, b=None):
    Counter.increase_count(player)
    if state.is_terminal(player) or depth == 0:
        return state.heuristics()
    U = state.successors(player)
    score = []
    for u in U:
        score.append(min_max(Board(u), depth - 1, -player))
    if player == 1:
        return max(score)
    if player == -1:
        return min(score)


def next_move(state: Board, depth=0, player=1, algorithm=min_max):
    if algorithm == rand_move:
        return rand_move(state)

    if player == 1:
        best_score = -20
    else:
        best_score = 20
    best_move = (None, None)
    for i in range(3):
        for j in range(3):
            if state.board[i][j].sign == "":
                state_dict = state.board_state()
                state_dict[i * 3 + j + 1] = player
                score = algorithm(Board(state_dict), depth, player, -100, 100)
                if player == 1:
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (i, j)
    # print(player, ":\t", best_move)
    return best_move


def rand_move(state: Board):
    available = state.list_available()
    move = choice(available)
    return (move - 1) // 3, (move - 1) % 3


def make_stats(algorithm1, algorithm2, trials, depth1=0, depth2=0):
    who_won = {-1: 0, 1: 0, "Draw": 0}
    searched_states = []
    for _ in range(trials):
        player = 1
        my_board = Board()
        won_by_player = False
        while not my_board.is_board_full():
            if player == 1:
                x, y = next_move(my_board, depth1, player, algorithm1)
            elif player == -1:
                x, y = next_move(my_board, depth2, player, algorithm2)
            my_board.change_state(x, y, player)
            # my_board.print_board()
            if my_board.player_won(player):
                won_by_player = True
                who_won[player] += 1
                break
            player *= -1
        searched_states.append(copy.deepcopy(Counter.return_count()))
        Counter.reset_count()
        if not won_by_player:
            who_won["Draw"] += 1
    dict_for_print = {min_max: "Algorytm Minimax", alpha_beta: "Algorytm Minimax \u03B1 - \u03B2",
                      rand_move: "AI losujący swój ruch", -1: "Gracz Min",
                      1: "Gracz Max", "Draw": "Remis"}
    print("Liczba prób:\t", trials, "\nGracz Max:\n\tZastosowany algorytm:\t", dict_for_print[algorithm1],
          "\n\tGłębokość:\t", depth1,
          "\nGracz Min:\n\tZastosowany algorytm:\t", dict_for_print[algorithm2], "\n\tGłębokość:\t", depth2,
          "\nWyniki:\n", "\tGracz Max", who_won[1], "\n\tGracz Min", who_won[-1], "\n\tRemis", who_won["Draw"],
          "\nPrzeszukane stany: \n", searched_states)


def main():
    make_stats(min_max, rand_move, 15, depth1=4)
    make_stats(min_max, min_max, 7, depth1=9, depth2=9)
    make_stats(min_max, alpha_beta, 7, depth1=9, depth2=9)
    make_stats(min_max, min_max, 7, depth1=9, depth2=3)
    make_stats(min_max, alpha_beta, 7, depth1=3, depth2=9)
    make_stats(min_max, min_max, 7, depth1=3, depth2=3)
    make_stats(min_max, alpha_beta, 7, depth1=3, depth2=3)
    make_stats(min_max, min_max, 7, depth1=1, depth2=0)
    make_stats(min_max, min_max, 7, depth1=0, depth2=9)
    make_stats(rand_move, rand_move, 20)


if __name__ == "__main__":
    main()


def test_field():
    my_field = Field(4)
    assert my_field.value == 4


def test_empty_board():
    empty_board = Board()
    assert empty_board.heuristics() == 0


def test_changing_state():
    my_board = Board()
    my_board.change_state(1, 1, -1)
    assert my_board.heuristics() == 4


def test_filled_board():
    my_board = Board({3: 1, 5: -1, 9: 1})
    assert my_board.heuristics() == 2


@pytest.mark.parametrize("state, is_full",
                         [
                             ({1: -1, 5: -1, 7: 1, 9: 1}, False),
                             ({1: 1, 2: -1, 3: -1, 4: 1, 5: 1, 6: -1, 7: 1, 8: -1, 9: 1}, True)
                         ])
def test_is_full(state, is_full):
    assert Board(state).is_board_full() == is_full


@pytest.mark.parametrize('state, player, is_terminal',
                         [
                             ({1: -1, 2: -1, 5: -1, 9: 1}, 1, False),
                             ({1: -1, 5: -1, 7: 1, 9: 1}, 1, False),
                             ({1: -1, 5: -1, 6: 1, 9: 1}, 1, False),
                             ({1: 1, 4: 1, 7: 1}, 1, True),  # first column
                             ({1: 1, 5: 1, 9: 1}, 1, True),  # diagonal
                             ({1: 1, 3: -1, 4: 1, 5: -1, 7: -1, 9: 1}, -1, True)  # diagonal O
                         ])
def test_terminal_states(state: dict, player, is_terminal):
    assert Board(state).is_terminal(player) == is_terminal


def test_successors():
    test_board = Board({1: 1, 2: -1, 3: -1, 5: 1, 6: -1, 7: 1, 8: -1})
    assert len(test_board.successors(-1)) == 2
    assert len(test_board.successors(1)) == 2
