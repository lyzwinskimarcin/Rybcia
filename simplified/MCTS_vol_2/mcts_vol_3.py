import random
import numpy as np
from .simulation_assistant import SimulationAssistant
from simplified.board import Board
from .node import Node


class MCTS:
    def __init__(self, n_rows, n_cols, number_of_penguins, iterations=1000, C_value=1.00):
        self.iterations = iterations
        self.simulation_assistant = SimulationAssistant(n_rows, n_cols, C_value)

        self.number_of_penguins = number_of_penguins
        self.starting_phase = True

        self.give_penguin_pos = True
        self.penguin_pos = None
        self.target_pos = None

    def check_if_starting_phase(self, board):

        # IF VERY UNLUCKY PENGUIN MIGHT BE PLACED IN A NOT MOVABLE POSITON AND IT GOES WRONG REPAIR IT LATER
        penguins_on_the_board = len(np.argwhere(board.player_board != 0))
        return True if penguins_on_the_board < 2 * self.number_of_penguins else False

    def get_pos(self, board):
        self.simulation_assistant.get_board_state(board)
        if self.check_if_starting_phase(board):
            # Choose starting positions
            valid_positions = self.simulation_assistant.assist_board.get_valid_starting_positions()
            starting_pos = random.sample(valid_positions, 1)[0]
            return starting_pos
        else:
            if self.give_penguin_pos:
                self.do_search(self.simulation_assistant.assist_board)
                self.give_penguin_pos = not self.give_penguin_pos
                return self.penguin_pos
            else:
                self.give_penguin_pos = not self.give_penguin_pos
                return self.target_pos

    def do_search(self, board):
        iteration = 0
        # Create a root node
        moves_to_expand = board.get_penguins_positions(board.player_turn)
        root_node = Node(parent=None, move=None, board=board, moves_to_expand=moves_to_expand,
                         is_terminal=False, is_penguin_selected=False)
        while iteration < self.iterations:
            self.one_iteration(root_node)
            iteration += 1
            # if iteration % 10 == 0:
            #     print(iteration)
        strongest_node = root_node.select_strongest_child()
        self.penguin_pos = strongest_node.move
        self.target_pos = strongest_node.select_strongest_child().move

        # Printing out top 3 moves below
        top_moves = self.get_top_moves(root_node, 3)
        print(f"Penguin position: {root_node.select_strongest_child().move}")
        for key, value in top_moves.items():
            print( f"Move: {value} \nVal: {key}")
        print("################")
        # return penguin_pos, target_pos

    def one_iteration(self, root_node):
        node = root_node.single_run()
        if node.is_terminal:
            self.simulation_assistant.get_node_board(node)
            score = self.simulation_assistant.get_score(node.current_player)
            node.backpropagate(score)  # NEEDS SCORE!!!
        elif node.is_expandable():
            move = random.sample(node.moves_to_expand, 1)[0]
            node.moves_to_expand.remove(move)
            # USE SIMULATION ASSISTANT TO GET THE BOARD STATE
            self.simulation_assistant.get_node_board(node)
            # CREATE THE NODE
            node = self.simulation_assistant.expand_node(node, move)
            # PERFORM SIMULATION
            self.simulation_assistant.get_node_board(node)
            simulation_score = self.simulation_assistant.simulate(node.current_player)
            node.backpropagate(simulation_score)
        else:
            print("A this point in the code, the selected node should be either terminal or expandable")

    def get_top_moves(self, root_node, n_moves):
        penguin_node = root_node.select_strongest_child()
        top_moves = dict()
        if len(penguin_node.children) < n_moves:
            n_moves = len(penguin_node.children)
        for i in range(n_moves):
            child = penguin_node.select_strongest_child()
            penguin_node.children.remove(child)
            top_moves[child.val] = child.move
        return top_moves





