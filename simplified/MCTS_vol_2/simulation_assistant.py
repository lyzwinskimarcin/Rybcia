import random
from simplified.board import Board


class SimulationAssistant:
    def __init__(self, n_rows, n_cols, C_value):
        self.C_value = C_value
        self.assist_board = Board(n_rows, n_cols)
        self.penguin_selected = None

    def get_board_state(self, board):
        self.assist_board.fish_board = board.fish_board.copy()
        self.assist_board.player_board = board.player_board.copy()
        self.assist_board.available_tiles_board = board.available_tiles_board.copy()
        self.assist_board.player_turn = board.player_turn
        self.assist_board.player_1_fish = board.player_1_fish
        self.assist_board.player_2_fish = board.player_2_fish
        self.assist_board.player_1_tiles = board.player_1_tiles
        self.assist_board.player_2_tiles = board.player_2_tiles

    def get_node_board(self, node):
        self.assist_board.fish_board = node.fish_board.copy()
        self.assist_board.player_board = node.player_board.copy()
        self.assist_board.available_tiles_board = node.available_tiles_board.copy()

        self.assist_board.player_turn = node.current_player if node.is_penguin_selected else 3 - node.current_player
        self.assist_board.player_1_fish = node.player_1_fish
        self.assist_board.player_2_fish = node.player_2_fish
        self.assist_board.player_1_tiles = node.player_1_tiles
        self.assist_board.player_2_tiles = node.player_2_tiles
        if node.is_penguin_selected:
            self.penguin_selected = node.move
        else:
            self.penguin_selected = None

    def expand_node(self, parent, move):
        if self.penguin_selected is None:
            # check if is terminal
            is_terminal = True if self.assist_board.is_game_over() else False
            is_penguin_selected = True
            moves_to_expand = self.assist_board.check_valid_moves(move)
            child = parent.create_child(parent, move, self.assist_board, moves_to_expand, is_terminal,
                                        is_penguin_selected, C=self.C_value)
        else:
            self.assist_board.board_move(parent.move, move)
            is_terminal = True if self.assist_board.is_game_over() else False
            is_penguin_selected = False
            moves_to_expand = self.assist_board.get_penguins_positions(self.assist_board.player_turn)
            child = parent.create_child(parent, move, self.assist_board, moves_to_expand, is_terminal, is_penguin_selected)
        # Update value if is terminal
        if is_terminal:
            self.get_node_board(child)
            score = self.get_score(child.current_player)
            child.val = score

        return child

    def simulate(self, node_player_number):
        score = 0
        if self.assist_board.is_game_over():
            score = self.get_score(node_player_number)
            return score
        if self.penguin_selected is not None:
            target_move = random.sample(self.assist_board.check_valid_moves(self.penguin_selected), 1)[0]
            self.assist_board.board_move(self.penguin_selected, target_move)
            self.penguin_selected = None
            if self.assist_board.is_game_over():
                score = self.get_score(node_player_number)
            else:
                score = self.simulate(node_player_number)
        else:
            # Simulation if penguin is not selected
            running = True
            while running:
                if self.assist_board.is_game_over():
                    score = self.get_score(node_player_number)
                    break
                penguin_positions = self.assist_board.get_penguins_positions(self.assist_board.player_turn)
                penguin_pos = random.sample(penguin_positions, 1)[0]
                target_moves = self.assist_board.check_valid_moves(penguin_pos)
                if target_moves:
                    target_pos = random.sample(target_moves, 1)[0]
                else:
                    penguin_positions.remove(penguin_pos)
                    penguin_pos = penguin_positions[0]
                    target_pos = random.sample(self.assist_board.check_valid_moves(penguin_pos), 1)[0]
                self.assist_board.board_move(penguin_pos, target_pos)
        return score

    def get_score(self, node_player_number):
        who_won = self.assist_board.who_won()
        if who_won == 0:
            score = 0.5
        elif who_won == node_player_number:
            score = 1
        else:
            score = 0
        return score

    def recycle_node(self, node, board):
        self.get_node_board(node)
        penguins_positions = self.assist_board.get_penguins_positions(self.assist_board.player_turn)
        for pos in penguins_positions:
            if board.player_board[pos] != self.assist_board.player_turn:
                move_from = pos
                break
        new_positions = board.get_penguins_positions(self.assist_board.player_turn)
        penguins_positions = set(penguins_positions)
        for pos in new_positions:
            if pos not in penguins_positions:
                move_to = pos
                break
        for child in node.children:
            if child.move == move_from:
                penguin_node = child
                break
        for child in penguin_node.children:
            if child.move == move_to:
                recycled_node = child
                break
        return recycled_node
