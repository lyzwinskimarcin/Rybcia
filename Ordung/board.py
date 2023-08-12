import numpy as np

class Board:
    # Ideas for fields: number of tiles from the start, and left on the board, number of fish from start and left on the board
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.fish_board, self.player_board, self.available_tiles_board = self.initialize_boards()
        self.player_turn = 1

    def initialize_boards(self):
        """Initializes fish_board, player_board and available_tiles_board and returns them in that order"""
        shape = (self.n_rows, self.n_cols)

        # need to work on proportions, also there definitely need to be at least one 1 fish tile, preferably more
        # maybe define amounts and just place them?
        fish_board = np.random.randint(1, 4, shape)
        player_board = np.zeros(shape, dtype='int8')
        available_tiles_board = np.ones(shape, dtype='int8')
        return fish_board, player_board, available_tiles_board

    def choose_starting_position(self, player_number, row, col):
        """Takes x and y for starting position, changes the player_board and inserts given player_number"""
        self.get_valid_starting_positions()
        try:
            self.available_tiles_board[row][col] = 0
            self.player_board[row][col] = player_number
        except IndexError:
            print(f"Error: The position ({row}, {col}) is out of bounds.")
        return self.player_board

    def print_board(self, board):
        for i, row in enumerate(board):
            if i % 2 != 0:
                print(" ", end="")
            for cell in row:
                print(cell, end=" ")
            print()
        print("------------------------------------------")

    def board_move(self, player_number, penguin_row, penguin_col, target_row, target_col):
        self.player_board[penguin_row][penguin_col] = 0
        self.player_board[target_row][target_col] = player_number
        fish = self.fish_board[penguin_row][penguin_col]
        self.fish_board[penguin_row][penguin_col] = 0
        self.available_tiles_board[target_row][target_col] = 0
        self.player_turn = 2 if self.player_turn == 1 else 1
        return fish

    def get_valid_starting_positions(self):
        positions_of_ones = np.argwhere((self.fish_board == 1) & (self.player_board == 0))
        positions_of_ones_set = {(row, col) for row, col in positions_of_ones}
        return positions_of_ones_set
    def check_valid_moves(self, player_number):
        # might be updated after transforming valid_moves into a dictionary but does not have to be
        if not np.any(self.player_board == player_number):
            raise ValueError(f"Error: There is no player with number {player_number} on the board.")
        player_positions = np.argwhere(self.player_board == player_number)
        # print(player_positions)
        valid_moves = {}
        for pos in player_positions:
            elt = self.check_valid_moves_helper(pos)
            pos = tuple(pos)
            # valid moves stores lists of moves as values and positions of penguins as keys
            valid_moves[pos] = elt

        # For debugging
        # for lst in valid_moves:
        #     for pos in lst:
        #         print(pos)
        #         self.available_tiles_board[pos[0]][pos[1]] = 7

        return valid_moves

    def check_valid_moves_helper(self, position):
        """Helper function checking for valid moves for the given position and not for the player"""
        valid_moves_for_position = []
        col_step = 0
        # check the row to the left
        while 0 < col_step + position[1]:
            col_step -= 1
            if self.available_tiles_board[position[0]][position[1] + col_step] == 1:
                valid_moves_for_position.append([position[0], position[1] + col_step])
            else:
                break

        # check the row to the right
        col_step = 0
        while col_step + position[1] < self.n_cols - 1:
            col_step += 1
            if self.available_tiles_board[position[0]][position[1] + col_step] == 1:
                valid_moves_for_position.append([position[0], position[1] + col_step])
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
                valid_moves_for_position.append([d_row, d_col])
            else:
                break
            row_step -= 1
            col_step -= 1 if d_row % 2 == 0 else 0

        # check the negative diagonal to the right
        row_step = 1
        col_step = 0 if position[0] % 2 == 0 else 1
        while position[0] + row_step <= self.n_rows-1 and position[1] + col_step <= self.n_cols-1:
            d_row = position[0] + row_step
            d_col = position[1] + col_step  # these two are only needed to make the lines shorter
            if self.available_tiles_board[d_row][d_col] == 1:
                valid_moves_for_position.append([d_row, d_col])
            else:
                break
            row_step += 1
            col_step += 0 if d_row % 2 == 0 else 1




        # check the positive diagonal to the left
        row_step = 1
        col_step = -1 if position[0] % 2 == 0 else 0
        while position[0] + row_step <= self.n_rows-1 and 0 <= position[1] + col_step:
            d_row = position[0] + row_step
            d_col = position[1] + col_step  # these two are only needed to make the lines shorter
            if self.available_tiles_board[d_row][d_col] == 1:
                valid_moves_for_position.append([d_row, d_col])
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
                valid_moves_for_position.append([d_row, d_col])
            else:
                break
            row_step -= 1
            col_step += 0 if d_row % 2 == 0 else 1


        return valid_moves_for_position # this format: [[0,1], [1,0]]

    def get_penguin_number(self):
        return np.count_nonzero(self.player_board == 1)



# initialize_board(): Tworzy początkowy stan planszy.
# update_board(): Aktualizuje stan planszy po ruchu.
# get_tile_info(): Zwraca informacje o danym kafelku (np. liczba ryb, czy jest zajęty).
# get_valid_moves(): Zwraca listę możliwych ruchów dla danego gracza.
# make_move(): Wykonuje ruch na planszy.


# player_pos = np.argwhere(self.player_board == player_number)[0]

#
# Plansza = Board(5, 5)
# Plansza.choose_starting_position(0, 3, 1)
# Plansza.choose_starting_position(1, 1, 2)
# Plansza.choose_starting_position(2, 2, 2)
#
#
# boards = [Plansza.fish_board, Plansza.player_board, Plansza.available_tiles_board]
# for plansza in boards:
#     Plansza.print_board(plansza)
#
# Plansza.print_board(Plansza.available_tiles_board)
#
# print(Plansza.check_valid_moves(1))
# # print(Plansza.check_valid_moves(2))
#
# Plansza.print_board(Plansza.available_tiles_board)





