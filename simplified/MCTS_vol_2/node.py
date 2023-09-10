import random
import math


class Node:
    # Maybe it is better to give the whole board just for the creation
    def __init__(self, parent, move, board, moves_to_expand, is_terminal, is_penguin_selected, C=1.00):
        self.vis = 0
        self.val = 0

        self.C = C

        self.fish_board = board.fish_board
        self.player_board = board.player_board
        self.available_tiles_board = board.available_tiles_board

        self.player_1_fish = board.player_1_fish
        self.player_2_fish = board.player_2_fish
        self.player_1_tiles = board.player_1_tiles
        self.player_2_tiles = board.player_2_tiles

        self.parent = parent
        self.children = set()

        self.move = move
        self.current_player = board.player_turn
        self.is_penguin_selected = is_penguin_selected

        self.moves_to_expand = moves_to_expand
        self.is_terminal = is_terminal   # needs to be checked
        #self.is_expandable = True # Untill there are moves_to_expand it's useless

    def create_child(self, parent, move, board, moves_to_expand, is_terminal, is_penguin_selected, C=1.00):
        child = Node(parent, move, board, moves_to_expand, is_terminal, is_penguin_selected, C=C)
        self.children.add(child)
        if is_terminal:
            child.val = 1
        return child   # is that necessary?

    def ucb(self):
        # if self.vis == 0:
        #     return math.inf  # favor exploration of unvisited nodes
        avg_val = self.val / self.vis  # Average value
        exploration_term = self.C * math.sqrt(math.log(self.parent.vis) / self.vis)
        return avg_val + exploration_term

    def single_run(self):
        if self.is_terminal or self.is_expandable():
            return self
        node = self.select_child().single_run()
        return node

    def select_child(self):
        child = max(self.children, key=lambda node: node.ucb())
        return child

    def is_expandable(self):
        return True if len(self.moves_to_expand) > 0 else False

    def backpropagate(self, score):
        self.vis += 1
        self.val += score
        if self.parent is not None:
            self.parent.backpropagate(score * (-1))

    def select_strongest_child(self):
        strongest_child = max(self.children, key=lambda child: child.val)
        return strongest_child

