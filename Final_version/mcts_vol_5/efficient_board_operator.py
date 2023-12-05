import random
import numpy as np
from .node import Node
from Final_version.mcts_vol_5 import faster_methods
from Final_version.board import Board


class EfficientBoardOperator:
    def __init__(self, n_rows, n_cols, number_of_penguins):
        shape = (4, n_rows, n_cols)
        self.board = np.zeros(shape, dtype='int8')
        self.board[3][0][2] = number_of_penguins
        self.n_rows = n_rows
        self.n_cols = n_cols

    def get_node_state(self, node: Node):
        self.board = node.state.copy()

    def get_board_state(self, board: Board):
        self.board[0] = board.fish_board.copy()
        self.board[1] = board.player_board.copy()
        self.board[2] = board.available_tiles_board.copy()

        # getting the attributes

        self.board[3][0][0] = 1 if board.is_starting_phase else 0
        self.board[3][0][1] = board.player_turn
        self.board[3][0][3] = board.player_1_fish
        self.board[3][0][4] = board.player_2_fish

    def simulate(self):
        running = True
        while running:
            if self.is_game_over():
                faster_methods.game_over(self.board)
                break
            valid_moves = self.get_valid_moves()
            move = random.sample(valid_moves, 1)[0]
            self.move(move)


    # BOARD METHODS

    # Game logic methods

    def is_game_over(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return True
        else:
            return False

    def game_over(self):
        # Add fish that penguins are standing on
        player_1_positions = np.argwhere(self.board[1] == 1)
        player_1_positions = [tuple(pos) for pos in player_1_positions]
        for pos in player_1_positions:
            self.board[3][3] += self.board[0][pos]
        player_2_positions = np.argwhere(self.board[1] == 2)
        player_2_positions = [tuple(pos) for pos in player_2_positions]
        for pos in player_2_positions:
            self.board[3][3] += self.board[0][pos]

    def who_won(self):
        if self.board[3][0][3] > self.board[3][0][4]:
            return 1
        elif self.board[3][0][3] < self.board[3][0][4]:
            return 2
        else:
            return 0

    # Move checking methods

    def get_valid_moves(self):
        valid_moves = set()
        if self.board[3][0][0] == 1:
            valid_moves = faster_methods.get_valid_starting_moves(self.board)
        else:
            valid_moves = faster_methods.get_valid_penguin_moves(self.board, self.n_rows, self.n_cols)
        return valid_moves

    def get_valid_starting_moves(self):
        positions_of_ones = np.argwhere((self.board[0] == 1) & (self.board[2] == 1))
        positions_of_ones_set = {(row, col) for row, col in positions_of_ones}
        return positions_of_ones_set

    def get_valid_penguin_moves(self):
        valid_moves = set()
        penguins_positions = np.argwhere(self.board[1] == self.board[3][0][1])
        positions = [tuple(pos) for pos in penguins_positions]
        for position in positions:
            # check the row to the left
            col_step = 0
            while 0 < col_step + position[1]:
                col_step -= 1
                if self.board[2][position[0]][position[1] + col_step] == 1:
                    valid_moves.add((position, (position[0], position[1] + col_step)))

                else:
                    break

            # check the row to the right
            col_step = 0
            while col_step + position[1] < self.n_cols - 1:
                col_step += 1
                if self.board[2][position[0]][position[1] + col_step] == 1:
                    valid_moves.add((position, (position[0], position[1] + col_step)))

                else:
                    break

            # DIAGONALS

            # check the negative diagonal to the left
            row_step = -1
            col_step = -1 if position[0] % 2 == 0 else 0
            while position[0] + row_step >= 0 and 0 <= position[1] + col_step:
                d_row = position[0] + row_step
                d_col = position[1] + col_step  # these two are only needed to make the lines shorter
                if self.board[2][d_row][d_col] == 1:
                    valid_moves.add((position, (d_row, d_col)))
                else:
                    break
                row_step -= 1
                col_step -= 1 if d_row % 2 == 0 else 0

            # check the negative diagonal to the right
            row_step = 1
            col_step = 0 if position[0] % 2 == 0 else 1
            while position[0] + row_step <= self.n_rows - 1 and position[1] + col_step <= self.n_cols - 1:
                d_row = position[0] + row_step
                d_col = position[1] + col_step  # these two are only needed to make the lines shorter
                if self.board[2][d_row][d_col] == 1:
                    valid_moves.add((position, (d_row, d_col)))
                else:
                    break
                row_step += 1
                col_step += 0 if d_row % 2 == 0 else 1

            # check the positive diagonal to the left
            row_step = 1
            col_step = -1 if position[0] % 2 == 0 else 0
            while position[0] + row_step <= self.n_rows - 1 and 0 <= position[1] + col_step:
                d_row = position[0] + row_step
                d_col = position[1] + col_step  # these two are only needed to make the lines shorter
                if self.board[2][d_row][d_col] == 1:
                    valid_moves.add((position, (d_row, d_col)))
                else:
                    break
                row_step += 1
                col_step -= 1 if d_row % 2 == 0 else 0

            # check the negative diagonal to the right
            row_step = -1
            col_step = 0 if position[0] % 2 == 0 else 1
            while position[0] + row_step >= 0 and position[1] + col_step <= self.n_cols - 1:
                d_row = position[0] + row_step
                d_col = position[1] + col_step  # these two are only needed to make the lines shorter
                if self.board[2][d_row][d_col] == 1:
                    valid_moves.add((position, (d_row, d_col)))
                else:
                    break
                row_step -= 1
                col_step += 0 if d_row % 2 == 0 else 1

        return valid_moves

    # Move making methods

    def move(self, move: tuple):
        """Needs a position as a tuple in the starting phase  (row, col)
         or a tuple of two tuples in the middle game.
         ((penguin_row, penguin_col), (target_row, target_col)"""
        if self.board[3][0][0]:
            faster_methods.starting_move(self.board, move)
        else:
            faster_methods.middle_game_move(self.board, move)
            # Switches turn if the other player has no move
            if not self.get_valid_moves():
                self.board[3][0][1] = 3 - self.board[3][0][1]


    def starting_move(self, move):
        self.board[1][move] = self.board[3][0][1]
        self.board[2][move] = 0
        # Turn change
        self.board[3][0][1] = 3 - self.board[3][0][1]

        if np.count_nonzero(self.board[1]) == self.board[3][0][2]:
            self.board[3][0][0] = False

    def middle_game_move(self, move):
        penguin_pos = move[0]
        target_pos = move[1]
        if self.board[3][0][1] == 1:
            self.board[3][0][3] += self.board[0][penguin_pos]
            self.board[0][penguin_pos] = 0
            self.board[1][penguin_pos] = 0
            self.board[1][target_pos] = 1
            self.board[2][target_pos] = 0
        elif self.board[3][0][1] == 2:
            self.board[3][0][4] += self.board[0][penguin_pos]
            self.board[0][penguin_pos] = 0
            self.board[1][penguin_pos] = 0
            self.board[1][target_pos] = 2
            self.board[2][target_pos] = 0
        # Turn change
        self.board[3][0][1] = 3 - self.board[3][0][1]

        # If there are no valid moves for the player the turn is switched up again
        if not self.get_valid_moves():
            self.board[3][0][1] = 3 - self.board[3][0][1]
