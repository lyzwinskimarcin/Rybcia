from final_version.mcts.node import Node
import random
from final_version.mcts.efficient_board_operator import EfficientBoardOperator
from final_version.mcts.faster_methods import who_won


class MCTS:
    def __init__(self, n_rows, n_cols, number_of_penguins, iterations=20000, C_value=0.8):
        self.iterations = iterations
        self.C = C_value
        self.vis_threshold = 10
        self.draw_value = 0.4

        self.board_operator = EfficientBoardOperator(n_rows, n_cols, number_of_penguins)

        # Node to recycle
        self.node_to_recycle = None

        # Storing the center of the board (useful for forcing center moves at the start)
        self.board_center = ((n_rows + 1)//2, (n_rows + 1)//2)

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if len(valid_moves) == 1:
            move = valid_moves.pop()
        else:
            move = self.do_search(board)
        return move

    def do_search(self, board):
        # Create a root node
        root_node = None
        if self.node_to_recycle is not None:
            root_node = self.recycle_node(board)
            root_node.parent = None
        if root_node is None:
            current_player = 3 - board.player_turn
            moves_to_expand = board.get_valid_moves()
            self.board_operator.get_board_state(board)
            root_node = Node(board= self.board_operator.board, parent=None,
                             move=None, current_player=current_player,
                             moves_to_expand=moves_to_expand, limiting_moves={}, is_terminal=False, C=self.C)

        iteration = 0
        while iteration < self.iterations:
            self.single_run(root_node)
            iteration += 1
        strongest_child = root_node.select_strongest_child()
        self.node_to_recycle = strongest_child

        # Print out top 3 moves
        strongest_children = sorted(root_node.children, key=lambda child: child.val, reverse=True)[:3]
        for child in strongest_children:
            print(f"Move: {child.move}")
            print(f"Value: {child.val}")

        return strongest_child.move

    def single_run(self, node):
        if node.is_expandable() and node.parent is None:
            self.expand_and_simulate(node)
            return
        elif node.is_expandable() and not node.parent.is_expandable() and node.parent.parent is None:
            self.expand_and_simulate(node)
            return
        elif node.is_expandable() and node.vis < self.vis_threshold:
            self.expand_and_simulate(node)
            return
        elif (
                node.is_expandable()
                and node.parent is not None
                and all(child.vis >= self.vis_threshold for child in node.parent.children)
        ):
            self.expand_and_simulate(node)
            return
        elif node.is_terminal:
            node.backpropagate(node.val)
            return
        node = node.select_child()
        self.single_run(node)

    def expand_and_simulate(self, node):
        self.board_operator.get_node_state(node)
        # Expand new node
        node = self.expand_node(node)
        # Simulate
        if node.is_terminal:
            score = node.val
        else:
            self.board_operator.simulate()
            score = self.get_score(node.current_player)
        node.backpropagate(score)

    def expand_node(self, node):
        # Expansion starting with limiting moves if possible
        if not node.limiting_moves:
            move = random.sample(node.moves_to_expand, 1)[0]
        else:
            move = random.sample(node.limiting_moves, 1)[0]
            node.limiting_moves.remove(move)

        self.board_operator.move(move)
        current_player = 3 - self.board_operator.board[3][0][1]
        moves_to_expand = self.board_operator.get_valid_moves()
        if self.board_operator.board[3][0][0] == 0:
            limiting_moves = self.board_operator.find_limiting_moves()
        else:
            limiting_moves = {}
        is_terminal = True if self.board_operator.is_game_over() else False
        child = Node(self.board_operator.board, node, move, current_player,
                     moves_to_expand,limiting_moves, is_terminal, node.C)
        if is_terminal:
            child.val = self.get_score(current_player)
        node.children.add(child)
        node.moves_to_expand.remove(move)
        return child

    def get_score(self, node_player_number):
        winner = who_won(self.board_operator.board)
        if winner == 0:
            score = self.draw_value
        elif winner == node_player_number:
            score = 1
        else:
            score = 0
        return score

    def recycle_node(self, board):
        """Choosing the right branch of the search tree to reuse based on opponent move"""
        for child in self.node_to_recycle.children:
            # That's where opponent's penguin should stand on the board:
            new_penguin_position = child.move if self.node_to_recycle.state[3][0][0] else child.move[1]
            if board.player_board[new_penguin_position] == 3 - board.player_turn:
                return child






