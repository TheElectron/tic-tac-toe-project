import random
import itertools
import numpy as np
from transform import Transform, Identity, Rotate90, Flip

# Constants and matrix transformations
BOARD_SIZE = 3
BOARD_DIMENSIONS = (BOARD_SIZE, BOARD_SIZE)

CELL_X = 1
CELL_O = -1
CELL_EMPTY = 0
RESULT_DRAW = 0
RESULT_X_WINS = 1
RESULT_O_WINS = -1
RESULT_NOT_OVER = 2

NEW_BOARD = np.array([CELL_EMPTY] * BOARD_SIZE ** 2)

TRANSFORMATIONS = [Identity(), Rotate90(1), Rotate90(2), Rotate90(3), Flip(np.flipud), Flip(np.fliplr), 
                Transform(Rotate90(1), Flip(np.flipud)), Transform(Rotate90(1), Flip(np.fliplr))]


# Auxiliary functions
def get_symmetrical_board_orientations(board_2d):
    return [(t.transform(board_2d), t) for t in TRANSFORMATIONS]


def get_rows_cols_and_diagonals(board_2d):
    rows_and_diagonal = get_rows_and_diagonal(board_2d)
    cols_and_antidiagonal = get_rows_and_diagonal(np.rot90(board_2d))
    return rows_and_diagonal + cols_and_antidiagonal


def get_rows_and_diagonal(board_2d):
    num_rows = board_2d.shape[0]
    return ([row for row in board_2d[range(num_rows), :]] + [board_2d.diagonal()])


def get_symbol(cell):
    if cell == CELL_X:
        return 'X'
    if cell == CELL_O:
        return 'O'
    return '-'


class Board:
    def __init__(self, illegal_move=None):
        self.count = 0
        self.board = np.copy(NEW_BOARD)
        self.board_2d = self.board.reshape(BOARD_DIMENSIONS)       
        self.illegal_move = illegal_move
    # Vizualize board
    def get_board_as_string(self):
        rows, cols = self.board_2d.shape
        board_as_string = "-------\n"
        for r in range(rows):
            for c in range(cols):
                move = get_symbol(self.board_2d[r, c])
                if c == 0:
                    board_as_string += f"|{move}|"
                elif c == 1:
                    board_as_string += f"{move}|"
                else:
                    board_as_string += f"{move}|\n"
        board_as_string += "-------\n"
        return board_as_string
    def show_board(self):
        print(self.get_board_as_string())
    def get_turn(self):
        return CELL_X if self.count % 2 == 0 else CELL_O
    def get_valid_moves(self):
        return ([i for i in range(self.board.size) if self.board[i] == CELL_EMPTY])
    def get_illegal_move_indexes(self):
        return ([i for i in range(self.board.size) if self.board[i] != CELL_EMPTY])
    def get_random_move(self):
        return random.choice(self.get_valid_moves())
    def play_move(self, move_index):
        if move_index not in self.get_valid_moves():
            self.illegal_move = move_index
        else:
            self.board[move_index] = self.get_turn()
            self.count += 1
    def get_game_result(self):
        if self.illegal_move is not None:
            return RESULT_O_WINS if self.get_turn() == CELL_X else RESULT_X_WINS
        rows_cols_and_diagonals = get_rows_cols_and_diagonals(self.board_2d)
        sums = list(map(sum, rows_cols_and_diagonals))
        max_value = max(sums)
        min_value = min(sums)
        if max_value == BOARD_SIZE:
            return RESULT_X_WINS
        if min_value == -BOARD_SIZE:
            return RESULT_O_WINS
        if CELL_EMPTY not in self.board_2d:
            return RESULT_DRAW
        return RESULT_NOT_OVER
    def is_gameover(self):
        return self.get_game_result()
        



def play_game():
    board = Board()
    print("sadasdas")
    while board.is_gameover() == RESULT_NOT_OVER:
        print("sadasdas")
        board.play_move(board.get_random_move())
        board.show_board()
    print("\n!!!!  X WINS  !!!!\n") if board.is_gameover() == RESULT_X_WINS else print("\n!!!!  O WINS  !!!!\n") 

play_game()
