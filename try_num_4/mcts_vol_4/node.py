import numpy as np


class Node:
    def __init__(self, parent, move, moves_to_expand, is_terminal):
        self.vis = 0
        self.val = 0

        self.parent = parent
        self.children = set()

        self.move = move
        self.who_made_move
        self.moves_to_expand = moves_to_expand
        self.is_terminal = is_terminal










