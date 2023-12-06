import math


class Node:
    def __init__(self, board, parent, move, current_player, moves_to_expand, is_terminal, C=1.00):
        self.vis = 0
        self.val = 0

        self.state = board.copy()

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
        if self.state[3][0][0] == 0:
            strongest_child = max(self.children, key=lambda child: child.val)
        else:
            num_of_favored_moves = 2
            n_rows = self.state.shape[1]
            n_cols = self.state.shape[2]
            print(self.state.shape)

            center = ((n_rows) // 2, (n_cols) // 2)


            def distance_to_center(node):
                move = node.move
                return (move[0] - center[0]) ** 2 + (move[1] - center[1]) ** 2

            closest_nodes = sorted(self.children, key=distance_to_center)[:num_of_favored_moves]
            strongest_child = max(closest_nodes, key=lambda child: child.val)
            print(center)
        return strongest_child






