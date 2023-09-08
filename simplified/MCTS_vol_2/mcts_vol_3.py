import random
import numpy as np
from simulation_assistant import SimulationAssistant
from simplified.board import Board
from node import Node


class MCTS:
    def __init__(self, n_rows, n_cols, number_of_penguins, iterations=100):
        self.iterations = iterations
        self.simulation_assistant = SimulationAssistant(n_rows, n_cols)

        self.number_of_penguins = number_of_penguins
        self.starting_phase = True

        self.give_penguin_pos = True
        self.penguin_pos = None
        self.target_pos = None

    def check_if_starting_phase(self, board):


    def get_pos(self, board):
        if self.starting_phase:
            # Choose starting positions
            valid_positions
        else:
            if self.give_penguin_pos:
                self.do_search(board)
                self.give_penguin_pos = not self.give_penguin_pos
                return self.penguin_pos
            else:
                return self.target_pos

    def do_search(self, board):
        iteration = 0
        # Create a root node
        moves_to_expand = board.get_penguins_positions(board.player_turn)
        root_node = Node(parent=None, move=None, board=board, moves_to_expand=moves_to_expand,
                         is_terminal=False, is_penguin_selected=False)
        while iteration < self.iterations:
            self.one_iteration(root_node)
        strongest_node = root_node.select_child()
        self.penguin_pos = strongest_node.move
        self.target_pos = strongest_node.select_child.move
        # return penguin_pos, target_pos





    def one_iteration(self, root_node):
        # GET ME A CHILD
        node = root_node.single_run()
        if node.is_terminal:
            node.backpropagate()  # NEEDS SCORE!!!
        elif node.is_expandable():
            move = random.sample(node.moves_to_expand)
            node.moves_to_expand.remove(move)
            # USE SIMULATION ASSISTANT TO GET THE BOARD STATE
            self.simulation_assistant.get_node_board(node)
            # CREATE THE NODE
            node = self.simulation_assistant.expand_node(move)
            # PERFORM SIMULATION
            simulation_score = self.simulation_assistant.simulate()
            node.backpropagate(simulation_score)
        else:
            print("A this point in the code, the selected node should be either terminal or expandable")





