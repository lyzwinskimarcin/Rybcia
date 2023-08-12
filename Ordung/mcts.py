import numpy as np
from board import Board

class MCTS:
    def __init__(self, board):
        self.draft_board = Board(board.n_rows, board.n_cols)
        self.draft_board.fish_board = board.fish_board
        self.draft_board.player_board = board.player_board
        self.draft_board.available_tiles_board = board.available_tiles_board

    def get_node_position(self, node):
        self.draft_board.fish_board = node.fish_board
        self.draft_board.player_board = node.player_board
        self.draft_board.available_tiles_board = node.available_tiles_board

    def expand_node(self, node):
        self.draft_board

    def simulate(self, node):
        return node

    def make_move_for_expansion(self):












