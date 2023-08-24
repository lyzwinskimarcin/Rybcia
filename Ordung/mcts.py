import numpy as np
from board import Board
import random

class MCTS:
    def __init__(self, board):
        self.draft_board = Board(board.n_rows, board.n_cols)
        self.draft_board.fish_board = board.fish_board
        self.draft_board.player_board = board.player_board
        self.draft_board.available_tiles_board = board.available_tiles_board
        self.draft_board.player_turn = board.player_turn
        # used for a trick in "get_mcts_move()"
        self.give_penguin_pos = True

    def get_node_position(self, node):
        self.draft_board.fish_board = node.fish_board
        self.draft_board.player_board = node.player_board
        self.draft_board.available_tiles_board = node.available_tiles_board

    def expand_node(self, node):
        self.get_node_position(node)
        self.make_move_for_expansion()

    def simulate(self, node):
        return node

    def make_move_for_expansion(self):
        # make a random move on the draft_board (not actual game board) and create a node based on that board
        pass

    def get_mcts_starting_pos(self, board):
        move = random.sample(board.get_valid_starting_positions(), 1)[0]
        return move[0], move[1]

    def get_mcts_move(self, board):
        # mcts stuff
        valid_moves = board.check_valid_moves(board.player_turn)
        print("coś")
        penguin_positions = valid_moves.keys()
        penguin_positions_pool = set()
        for pos in penguin_positions:
            if len(valid_moves[pos]) > 0:
                penguin_positions_pool.add(pos)
        penguin_pos = random.sample(penguin_positions_pool, 1)[0]

        target_pos = random.sample(valid_moves[penguin_pos], 1)[0]

        if self.give_penguin_pos:
            self.give_penguin_pos = False
            return penguin_pos[0], penguin_pos[1]
        else:
            self.give_penguin_pos = True
            return target_pos[0], target_pos[1]

    def dummy_mcts(self, board):
        valid_moves = board.check_valid_moves(board.player_turn)
        print("coś")
        penguin_positions = valid_moves.keys()
        penguin_pos = random.sample(penguin_positions, 1)[0]

        target_pos = random.sample(valid_moves[penguin_pos], 1)[0]
        return penguin_pos, target_pos

    def get_move_to_consider(self, board):
        moves = set()
        valid_moves = board.check_valid_moves












