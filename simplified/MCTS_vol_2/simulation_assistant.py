from simplified.board import Board
from node import Node


class SimulationAssistant:
    def __init__(self, n_rows, n_cols):
        self.assist_board = Board(n_rows, n_cols)
        self.penguin_selected = None

    def get_node_board(self, node):
        self.assist_board.fish_board = node.fish_board
        self.assist_board.player_board = node.player_board
        self.assist_board.available_tiles_board = node.available_tiles_board
        self.assist_board.player_turn = node.current_player
        self.assist_board.player_1_fish = node.player_1_fish
        self.assist_board.player_2_fish = node.player_2_fish
        self.assist_board.player_1_tiles = node.player_1_tiles
        self.assist_board.player_2_tiles = node.player_2_tiles
        if node.is_penguin_selected:
            self.penguin_selected = node.move

    def expand_node(self, parent, move):
        if self.penguin_selected is None:
            # check if is terminal
            is_terminal = False
            is_penguin_selected = True
            moves_to_expand = self.assist_board.check_valid_moves(move)
            parent.create_child(parent, move, self.assist_board, moves_to_expand, is_terminal, is_penguin_selected)
        else:
            self.assist_board.board_move(parent.move, move)
            is_terminal = True if self.assist_board.is_game_over() else False
            is_penguin_selected = False
            moves_to_expand = self.assist_board.get_penguins_positions(self.assist_board.player_turn)
            parent.create_child(parent, move, self.assist_board, moves_to_expand, is_terminal, is_penguin_selected)

