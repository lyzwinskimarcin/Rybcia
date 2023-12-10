import numpy as np


class Board:
    def __init__(self, n_rows, n_cols, number_of_penguins):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.fish_board, self.player_board, self.available_tiles_board = self.initialize_boards()
        self.player_turn = 1
        self.player_1_fish = 0
        self.player_2_fish = 0
        self.player_1_tiles = 0
        self.player_2_tiles = 0

        self.number_of_penguins = number_of_penguins
        self.is_starting_phase = True

    def initialize_boards(self):
        """Initializes fish_board, player_board and available_tiles_board and returns them in that order"""
        shape = (self.n_rows, self.n_cols)
        total_tiles = self.n_rows * self.n_cols

        # Defining proportions
        prop_1_fish = 0.5  # 50% of the tiles
        prop_2_fish = 0.3  # 30% of the tiles
        prop_3_fish = 0.2  # 20% of the tiles

        # Calculating the number of tiles for each fish count
        num_1_fish_tiles = int(total_tiles * prop_1_fish)
        num_2_fish_tiles = int(total_tiles * prop_2_fish)
        num_3_fish_tiles = total_tiles - num_1_fish_tiles - num_2_fish_tiles  # Ensuring total count matches

        # Creating the board
        fish_board = np.array([1] * num_1_fish_tiles + [2] * num_2_fish_tiles + [3] * num_3_fish_tiles)
        np.random.shuffle(fish_board)  # Shuffle to randomize the board
        fish_board = fish_board.reshape(shape)
        player_board = np.zeros(shape, dtype='int8')
        available_tiles_board = np.ones(shape, dtype='int8')
        return fish_board, player_board, available_tiles_board

    # METHODS FOR GAME RULES

    def is_game_over(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return True
        else:
            return False

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


    def who_won(self):
        """Useful for mcts, returns player number that won or 0 if there is a draw"""
        if self.player_1_fish > self.player_2_fish:
            return 1
        elif self.player_1_fish < self.player_2_fish:
            return 2
        else:
            return 0

    # METHODS FOR MAKING MOVES

    def starting_move(self, move):
        self.player_board[move] = self.player_turn
        self.available_tiles_board[move] = 0
        # Turn change
        self.player_turn = 3 - self.player_turn

        if np.count_nonzero(self.player_board) == self.number_of_penguins:
            self.is_starting_phase = False

    def middle_game_move(self, move):
        penguin_pos = move[0]
        target_pos = move[1]
        if self.player_turn == 1:
            self.player_1_fish += self.fish_board[penguin_pos]
            self.player_1_tiles += 1
            self.fish_board[penguin_pos] = 0
            self.player_board[penguin_pos] = 0
            self.player_board[target_pos] = 1
            self.available_tiles_board[target_pos] = 0
        elif self.player_turn == 2:
            self.player_2_fish += self.fish_board[penguin_pos]
            self.player_2_tiles += 1
            self.fish_board[penguin_pos] = 0
            self.player_board[penguin_pos] = 0
            self.player_board[target_pos] = 2
            self.available_tiles_board[target_pos] = 0
        # Turn change
        self.player_turn = 3 - self.player_turn
        if not self.get_valid_moves():
            self.player_turn = 3 - self.player_turn

    def move(self, move: tuple):
        """Needs a position as a tuple in the starting phase  (row, col)
         or a tuple of two tuples in the middle game.
         ((penguin_row, penguin_col), (target_row, target_col)"""
        if self.is_starting_phase:
            self.starting_move(move)
        else:
            self.middle_game_move(move)

    # METHODS CHECKING FOR VALID MOVES

    def get_penguins_positions(self, player_number):
        penguins_positions = np.argwhere(self.player_board == player_number)
        # Convert to list of tuples
        penguins_positions_tuples = [tuple(pos) for pos in penguins_positions]
        return penguins_positions_tuples

    def get_valid_starting_positions(self):
        positions_of_ones = np.argwhere((self.fish_board == 1) & (self.player_board == 0)) # maybe better to use available tiles board?
        positions_of_ones_set = {(row, col) for row, col in positions_of_ones}
        return positions_of_ones_set

    def get_valid_penguin_moves(self):
        valid_moves = set()
        positions = self.get_penguins_positions(self.player_turn)
        for position in positions:
            # check the row to the left
            col_step = 0
            while 0 < col_step + position[1]:
                col_step -= 1
                if self.available_tiles_board[position[0]][position[1] + col_step] == 1:
                    valid_moves.add((position, (position[0], position[1] + col_step)))

                else:
                    break

            # check the row to the right
            col_step = 0
            while col_step + position[1] < self.n_cols - 1:
                col_step += 1
                if self.available_tiles_board[position[0]][position[1] + col_step] == 1:
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
                if self.available_tiles_board[d_row][d_col] == 1:
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
                if self.available_tiles_board[d_row][d_col] == 1:
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
                if self.available_tiles_board[d_row][d_col] == 1:
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
                if self.available_tiles_board[d_row][d_col] == 1:
                    valid_moves.add((position, (d_row, d_col)))
                else:
                    break
                row_step -= 1
                col_step += 0 if d_row % 2 == 0 else 1

        return valid_moves

    def get_valid_moves(self):
        if self.is_starting_phase:
            return self.get_valid_starting_positions()
        else:
            return self.get_valid_penguin_moves()

    # METHODS FOR CONSOLE VISUALISATION

    def print_board(self, board):
        for i, row in enumerate(board):
            if i % 2 != 0:
                print(" ", end="")
            for cell in row:
                print(cell, end=" ")
            print()
        print("------------------------------------------")

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



