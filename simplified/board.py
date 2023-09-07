import numpy as np
import random


class Board:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.fish_board, self.player_board, self.available_tiles_board = self.initialize_boards()
        self.player_turn = 1
        self.player_1_fish = 0
        self.player_2_fish = 0
        self.player_1_tiles = 0
        self.player_2_tiles = 0


    def initialize_boards(self):
        """Initializes fish_board, player_board and available_tiles_board and returns them in that order"""
        shape = (self.n_rows, self.n_cols)

        # need to work on proportions, also there definitely need to be at least one 1 fish tile, preferably more
        # maybe define amounts and just place them?
        fish_board = np.random.randint(1, 4, shape)
        player_board = np.zeros(shape, dtype='int8')
        available_tiles_board = np.ones(shape, dtype='int8')
        return fish_board, player_board, available_tiles_board

    def is_game_over(self):
        number_of_valid_moves = 0
        penguins_positions = np.argwhere(self.player_board != 0)
        for pos in penguins_positions:
            moves_lst = self.check_valid_moves(pos)
            number_of_valid_moves += len(moves_lst)
        return True if number_of_valid_moves == 0 else False

    # METHODS CHECKING FOR VALID MOVES

    def get_valid_starting_positions(self):
        positions_of_ones = np.argwhere((self.fish_board == 1) & (self.player_board == 0)) # maybe better to use available tiles board?
        positions_of_ones_set = {(row, col) for row, col in positions_of_ones}
        return positions_of_ones_set

    def get_penguins_positions(self, player_number):
        penguins_positions = np.argwhere(self.player_board == player_number)
        # Convert to list of tuples
        penguins_positions_tuples = [tuple(pos) for pos in penguins_positions]
        return penguins_positions_tuples

    def check_valid_moves(self, position):
        valid_moves_for_position = []
        col_step = 0
        # check the row to the left
        while 0 < col_step + position[1]:
            col_step -= 1
            if self.available_tiles_board[position[0]][position[1] + col_step] == 1:
                valid_moves_for_position.append((position[0], position[1] + col_step))
            else:
                break

        # check the row to the right
        col_step = 0
        while col_step + position[1] < self.n_cols - 1:
            col_step += 1
            if self.available_tiles_board[position[0]][position[1] + col_step] == 1:
                valid_moves_for_position.append((position[0], position[1] + col_step))
            else:
                break

        # DIAGONALS

        # check the negative diagonal to the left
        row_step = -1
        col_step = -1 if position[0] % 2 == 0 else 0
        while position[0] + row_step >= 0 and 0 <= position[1] + col_step:
            d_row = position[0] + row_step
            d_col = position[1] + col_step  # these two are only needed to make the lines shorter
            if self.available_tiles_board[d_row][d_col] == 1:
                valid_moves_for_position.append((d_row, d_col))
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
            if self.available_tiles_board[d_row][d_col] == 1:
                valid_moves_for_position.append((d_row, d_col))
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
            if self.available_tiles_board[d_row][d_col] == 1:
                valid_moves_for_position.append((d_row, d_col))
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
            if self.available_tiles_board[d_row][d_col] == 1:
                valid_moves_for_position.append((d_row, d_col))
            else:
                break
            row_step -= 1
            col_step += 0 if d_row % 2 == 0 else 1

        return valid_moves_for_position  # this format: [(0,1), (1,0)]

    # METHODS FOR MAKING A MOVE

    def choose_starting_position(self, pos):
        if pos not in self.get_valid_starting_positions():
            raise ValueError("The given position is not valid. You can only start on 1 fish tiles")
        try:
            self.available_tiles_board[pos[0]][pos[1]] = 0
            self.player_board[pos[0]][pos[1]] = self.player_turn
        except IndexError:
            print(f"Error: The position ({pos[0]}, {pos[1]}) is out of bounds.")
        self.player_turn = 2 if self.player_turn == 1 else 1

    def board_move(self, penguin_pos, target_pos):
        # Board move part
        self.player_board[penguin_pos] = 0
        self.player_board[target_pos] = self.player_turn
        fish = self.fish_board[penguin_pos]
        self.fish_board[penguin_pos] = 0
        self.available_tiles_board[target_pos] = 0
        # Count score part
        if self.player_turn == 1:
            self.player_1_fish += fish
            self.player_1_tiles += 1
        elif self.player_turn == 2:
            self.player_2_fish += fish
            self.player_2_tiles += 2
        self.player_turn = 2 if self.player_turn == 1 else 1

    # CONSOLE VISUALISATION METHODS

    def print_board(self, board):
        for i, row in enumerate(board):
            if i % 2 != 0:
                print(" ", end="")
            for cell in row:
                print(cell, end=" ")
            print()
        print("------------------------------------------")

    def game_over(self):
        # Add fish that penguins are standing on
        player_1_positions = self.get_penguins_positions(1)
        for pos in player_1_positions:
            self.player_1_fish += self.fish_board[pos]
        self.player_1_tiles += 1
        player_2_positions = self.get_penguins_positions(2)
        for pos in player_2_positions:
            self.player_2_fish += self.fish_board[pos]
        self.player_2_tiles += 1
        # Print out scores
        self.print_scores()

    def print_scores(self):
        if self.player_1_fish > self.player_2_fish:
            print("Player 1 won!")
        elif self.player_1_fish < self.player_2_fish:
            print("Player 2 won!")
        else:
            print("It was a draw")
        print(f"Player 1 fish number: {self.player_1_fish}")
        print(f"Player 1 tiles number: {self.player_1_tiles}")
        print(f"Player 2 fish number: {self.player_2_fish}")
        print(f"Player 2 tiles number: {self.player_2_tiles}")


# def print_boards(board):
#     board_lst = [board.fish_board, board.player_board, board.available_tiles_board]
#     for _ in board_lst:
#         board.print_board(_)
#
# board = Board(7, 8)
# print_boards(board)
# moves = board.get_valid_starting_positions()
# print(moves)
#
# print_boards(board)
# move1, move2 = random.sample(moves, 2)
# board.choose_starting_position(move1)
# print(board.get_valid_starting_positions())
# board.choose_starting_position(move2)
# print(board.get_valid_starting_positions())
# moves = board.check_valid_moves(move1)
# print(moves)
# move3, move4 = random.sample(moves, 2)
#
# board.board_move(move1, move3)
# print_boards(board)
# board.board_move(move2, move4)
# print_boards(board)




