import math


class Node:
    def __init__(self, board, parent, move, current_player, moves_to_expand,limiting_moves, is_terminal, C=1.00):
        self.vis = 0
        self.val = 0

        self.state = board.copy()

        self.parent = parent
        self.children = set()

        self.move = move
        self.current_player = current_player
        self.is_terminal = is_terminal
        self.moves_to_expand = moves_to_expand
        self.limiting_moves = limiting_moves

        self.C = C

    def is_expandable(self):
        return True if len(self.moves_to_expand) > 0 else False

    def ucb(self):
        exploration_term = self.C * math.sqrt(math.log(self.parent.vis) / self.vis)
        return self.val + exploration_term

    def select_child(self):
        child = max(self.children, key=lambda node: node.ucb())
        return child

    def backpropagate(self, score):
        self.vis += 1
        self.val = ((self.val * (self.vis - 1)) + score) / self.vis
        if self.parent is not None:
            if self.parent.current_player == self.current_player:
                self.parent.backpropagate(score)
            else:
                self.parent.backpropagate(1 - score)

    def select_strongest_child(self):
        if self.state[3][0][0] == 0:
            strongest_child = max(self.children, key=lambda child: child.val)
        else:
            # Forcing center moves for starting phase of the game
            num_of_favored_moves = 3
            n_rows = self.state.shape[1]
            n_cols = self.state.shape[2]

            center = (n_rows // 2, n_cols // 2)

            def distance_to_center(node):
                move = node.move
                return (move[0] - center[0]) ** 2 + (move[1] - center[1]) ** 2

            closest_nodes = sorted(self.children, key=distance_to_center)[:num_of_favored_moves]
            strongest_child = max(closest_nodes, key=lambda child: child.val)
        return strongest_child






