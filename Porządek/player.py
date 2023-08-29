from board import Board
from game_logic import GameLogic
from mcts import MCTS


class Player:
    def __init__(self, player_number, visualisation_type="console", control_type="console"):
        """Set "console" to control the game from console, "pygame" to control through pygame.
        You can set control_type to "AI" to play against AI"""
        self.player_number = player_number
        self.visualisation_type = visualisation_type
        self.control_type = control_type

    def set_mcts(self, board):
        self.mcts = MCTS(board)

    def set_pygameVisualiser(self, pygameVisualiser):
        self.pygameVisualiser = pygameVisualiser

    def player_move(self):
        pass

    def get_player_move(self, board, is_starting_pos=False):
        if self.control_type == "console":
            row, col = self.get_move_input()
        elif self.control_type == "pygame":
            row, col = self.pygameVisualiser.get_mouse_move()
        elif self.control_type == "AI" and is_starting_pos:
            row, col = self.mcts.get_mcts_starting_pos(board)
        elif self.control_type == "AI":
            row, col = self.mcts.get_mcts_move(board)
        valid_starting_moves = board.get_valid_starting_positions()
        if is_starting_pos:
            if (row, col) not in valid_starting_moves:
                print("Invalid starting positions were given")
                row, col = self.get_player_move(is_starting_pos, valid_starting_moves)

        return row, col

    def get_move_input(self):
        # Rows and columns counted from zero. To count them from one subtract 1 from each value
        print("Type the row: ")
        row = int(input())
        print("Type the column: ")
        col = int(input())
        return row, col










