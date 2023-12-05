from .node import Node
import random
from .efficient_board_operator import EfficientBoardOperator
from .faster_methods import who_won


class MCTS:
    def __init__(self, n_rows, n_cols, number_of_penguins, iterations=1000, C_value=1.00):
        self.iterations = iterations
        self.C = C_value
        self.vis_threshold = 10  # when to expand a node
        self.draw_value = 0.5

        self.board_operator = EfficientBoardOperator(n_rows, n_cols, number_of_penguins)

        # Node to recycle
        self.node_to_recycle = None

        # Storing the center of the board
        self.board_center =((n_rows + 1)//2, (n_rows + 1)//2)

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

        # This way if recycling fails root_node is still created
        if root_node is None:
            current_player = 3 - board.player_turn
            moves_to_expand = board.get_valid_moves()
            self.board_operator.get_board_state(board)
            root_node = Node(board= self.board_operator.board, parent=None,
                             move=None, current_player=current_player,
                             moves_to_expand=moves_to_expand, is_terminal=False, C=self.C)

        root_node.parent = None

        print("Przed:")
        print(root_node.moves_to_expand)

        iteration = 0
        while iteration < self.iterations:
            self.single_run(root_node)
            iteration += 1
        strongest_child = root_node.select_strongest_child()
        self.node_to_recycle = strongest_child

        print("Po:")
        print(root_node.moves_to_expand)

        return strongest_child.move

    def single_run(self, node):
        if node.is_expandable() and node.parent is None:
            self.expand_and_simulate(node)
            return
        elif node.is_expandable() and node.vis < self.vis_threshold:
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
        # Random expanding
        move = random.sample(node.moves_to_expand, 1)[0]

        self.board_operator.move(move)
        current_player = 3 - self.board_operator.board[3][0][1]
        moves_to_expand = self.board_operator.get_valid_moves()
        is_terminal = True if self.board_operator.is_game_over() else False
        child = Node(self.board_operator.board, node, move, current_player,
                     moves_to_expand, is_terminal, node.C)
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
        for child in self.node_to_recycle.children:
            # That's where opponent's penguin should stand on the board:
            new_penguin_position = child.move if self.node_to_recycle.state[3][0][0] else child.move[1]
            if board.player_board[new_penguin_position] == 3 - board.player_turn:
                return child






