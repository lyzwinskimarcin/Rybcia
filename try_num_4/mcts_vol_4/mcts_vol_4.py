from .node import Node
from try_num_4.board import Board
import random


class MCTS:
    def __init__(self, n_rows, n_cols, number_of_penguins, iterations=1000, C_value=1.00):
        self.iterations = iterations
        self.C = C_value
        self.vis_threshold = 10  # when to expand a node
        self.draw_value = 0.5

        self.draft_board = Board(n_rows, n_cols, number_of_penguins)


        # Node to recycle
        self.node_to_recycle = None

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

        if root_node is None:
            current_player = 3 - board.player_turn
            moves_to_expand = board.get_valid_moves()
            root_node = Node(parent=None, move=None, current_player=current_player,
                             moves_to_expand=moves_to_expand, is_terminal=False, C=self.C)
        self.copy_board(board)
        iteration = 0
        while iteration < self.iterations:
            self.single_run(root_node)
            self.copy_board(board)
            iteration += 1
        strongest_child = root_node.select_strongest_child()
        self.node_to_recycle = strongest_child
        return strongest_child.move

    def single_run(self, node):
        if node.is_expandable() and node.vis < self.vis_threshold:
            self.expand_and_simulate(node)
            return
        elif node.is_terminal:
            node.backpropagate(node.val)
            return
        node = node.select_child()
        self.draft_board.move(node.move)
        self.single_run(node)

    def expand_and_simulate(self, node):
        # Expand new node
        node = self.expand_node(node)
        # Simulate
        if node.is_terminal:
            score = node.val
        else:
            self.simulate()
            score = self.get_score(node.current_player)
        node.backpropagate(score)

    def expand_node(self, node):
        # PLACE FOR SMART EXPANDING

        # Random expanding
        move = random.sample(node.moves_to_expand, 1)[0]
        self.draft_board.move(move)
        current_player = 3 - self.draft_board.player_turn
        moves_to_expand = self.draft_board.get_valid_moves()
        is_terminal = True if self.draft_board.is_game_over() else False
        child = Node(node, move, current_player, moves_to_expand, is_terminal, node.C)
        if is_terminal:
            child.val = self.get_score(current_player)
        node.children.add(child)
        node.moves_to_expand.remove(move)
        return child

    def simulate(self):
        running = True
        while running:
            if self.draft_board.is_game_over():
                self.draft_board.game_over()
                break
            valid_moves = self.draft_board.get_valid_moves()
            move = random.sample(valid_moves, 1)[0]
            self.draft_board.move(move)

    def get_score(self, node_player_number):
        who_won = self.draft_board.who_won()
        if who_won == 0:
            score = self.draw_value
        elif who_won == node_player_number:
            score = 1
        else:
            score = 0
        return score

    def copy_board(self, board):
        self.draft_board.fish_board = board.fish_board.copy()
        self.draft_board.player_board = board.player_board.copy()
        self.draft_board.available_tiles_board = board.available_tiles_board.copy()
        self.draft_board.player_turn = board.player_turn
        self.draft_board.player_1_fish = board.player_1_fish
        self.draft_board.player_2_fish = board.player_2_fish
        self.draft_board.player_1_tiles = board.player_1_tiles
        self.draft_board.player_2_tiles = board.player_2_tiles
        self.draft_board.is_starting_phase = board.is_starting_phase

    def recycle_node(self, board):
        for child in self.node_to_recycle.children:
            # That's where opponent's penguin should stand on the board:
            new_penguin_position = child.move if self.draft_board.is_starting_phase else child.move[1]
            if board.player_board[new_penguin_position] == 3 - board.player_turn:
                return child









