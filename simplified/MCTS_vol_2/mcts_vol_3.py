import random
import numpy as np
from simulation_assistant import SimulationAssistant
from simplified.board import Board
from node import Node


class MCTS:
    def __init__(self, board):
        self.draft_board = Board(board.n_rows, board.n_cols)
        # Is it necessary? (below)
        self.draft_board.fish_board = board.fish_board
        self.draft_board.player_board = board.player_board
        self.draft_board.available_tiles_board = board.available_tiles_board
        self.draft_board.player_turn = board.player_turn

        self.player_turn = board.player_turn
        self.simulation_assistant = SimulationAssistant(board.n_rows, board.n_cols)

    def do_search(self):
        pass

    def one_iteration(self, root_node):
        # GET ME A CHILD
        node = root_node.single_run()
        if node.is_terminal:
            node.backpropagate()
        elif node.is_expandable():
            move = random.sample(node.moves_to_expand)
            node.moves_to_expand.remove(move)
            # USE SIMULATION ASSISTANT TO GET THE BOARD STATE
            self.simulation_assistant.get_node_board(node)
            # CREATE THE NODE
            node = self.simulation_assistant.expand_node(move)
            # PERFORM SIMULATION

        else:
            print("A this point in the code, the selected node should be either terminal or expandable")





