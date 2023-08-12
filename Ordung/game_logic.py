import numpy as np
from board import Board


class GameLogic:
    player_1_tiles = 0
    player_2_tiles = 0
    player_1_fish = 0
    player_2_fish = 0
    visualisation_on = False

    def __init__(self, n_rows=8, n_cols=7):
        self.board = Board(n_rows, n_cols)

    def is_game_over(self):
        number_of_valid_moves = 0
        for _ in range(1, 3):
            valid_moves = self.board.check_valid_moves(_)
            for moves_lst in valid_moves.values():
                number_of_valid_moves += len(moves_lst)
        return True if number_of_valid_moves == 0 else False

    def choose_starting_position(self, player_number, row, col):
        self.board.choose_starting_position(player_number, row, col)

    def make_move(self, player_number, penguin_row, penguin_col, target_row, target_col):
        # Checking if the given values are valid
        _player = self.board.player_board[penguin_row][penguin_col]
        if not _player == player_number:
            raise ValueError(f"Error: The player standing on this position is {_player}")
        valid_moves = self.board.check_valid_moves_helper((penguin_row, penguin_col))
        if not [target_row, target_col] in valid_moves:
            raise ValueError(f"Error: The given move is not valid!")

        # Making the move on the board
        fish = self.board.board_move(player_number, penguin_row, penguin_col, target_row, target_col)
        self.add_score(fish, player_number)

    def add_score(self, fish, player_number):
        if player_number == 1:
            self.player_1_fish += fish
            self.player_1_tiles += 1
        elif player_number == 2:
            self.player_2_fish += fish
            self.player_2_tiles += 1


    def game_over(self):
        if self.player_1_fish > self.player_2_fish:
            print("Player 1 won!")
        elif self.player_1_fish < self.player_2_fish:
            print("Player 2 won!")
        else:
            print("It was a draw")
        self.print_scores()

    def print_scores(self):
        print(f"Player 1 fish number: {self.player_1_fish}")
        print(f"Player 1 tiles number: {self.player_1_tiles}")
        print(f"Player 2 fish number: {self.player_2_fish}")
        print(f"Player 2 tiles number: {self.player_2_tiles}")























