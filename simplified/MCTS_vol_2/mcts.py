import numpy as np
from Porządek.board import Board


class MCTS:
    def __init__(self, board):
        self.draft_board = Board(board.n_rows, board.n_cols)
        # Is it necessary? (below)
        self.draft_board.fish_board = board.fish_board
        self.draft_board.player_board = board.player_board
        self.draft_board.available_tiles_board = board.available_tiles_board
        self.draft_board.player_turn = board.player_turn

        self.player_turn = board.player_turn

    def do_search(self, board):
        self.setup_draft_board(board)
        do_search = True
        while do_search:
            penguins = self.present_penguins()






    def present_penguins(self):
        penguin_positons = np.argwhere(self.draft_board.player_board == self.player_turn)
        print(penguin_positons)
        return penguin_positons

    def present_available_moves(self, penguin_pos):
        return self.draft_board.check_valid_moves_helper(penguin_pos)

    def setup_draft_board(self, board):
        self.draft_board.fish_board = board.fish_board
        self.draft_board.player_board = board.player_board
        self.draft_board.available_tiles_board = board.available_tiles_board
        self.draft_board.player_turn = board.player_turn

        self.player_turn = board.player_turn















