import math


class Node:
    def __init__(self, parent, move, current_player, moves_to_expand, is_terminal, C=1.00):
        self.vis = 0
        self.val = 0

        self.parent = parent
        self.children = set()

        self.move = move
        self.current_player = current_player
        self.moves_to_expand = moves_to_expand
        self.is_terminal = is_terminal

        self.C = C

    def is_expandable(self):
        return True if len(self.moves_to_expand) > 0 else False

    def ucb(self):
        if self.vis == 0:
            return math.inf  # favor exploration of unvisited nodes
        exploration_term = self.C * math.sqrt(math.log(self.parent.vis) / self.vis)
        return self.val + exploration_term

    def select_child(self):
        child = max(self.children, key=lambda node: node.ucb())
        return child

    def backpropagate(self, score):
        self.vis += 1
        self.val = ((self.val * (self.vis - 1)) + score) / self.vis
        if self.parent is not None:
            self.parent.backpropagate(1 - score)

    def select_strongest_child(self):
        strongest_child = max(self.children, key=lambda child: child.val)
        return strongest_child






