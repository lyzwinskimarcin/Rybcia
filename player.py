from board import Board
from game_logic import GameLogic


class Player:
    def __init__(self, player_number, visualisation_type="console", control_type="console"):
        """Set "console" to control the game from console, "pygame" to control through pygame.
        You can set control_type to "AI" to play against AI"""
        self.player_number = player_number
        self.visualisation_type = visualisation_type
        self.control_type = control_type

    def set_gameVisualiser(self, gameVisualiser):
        self.gameVisualiser = self.get_gameVisualiser()

    def player_move(self):
        pass

    def get_player_move(self):
        if self.control_type == "console":
            row, col = self.get_move_input()
        elif self.control_type == "pygame":
            row, col = self.gameVisualiser.get_mouse_move()
        # AI moves should be connected HERE

    def get_move_input(self):
        # Rows and columns counted from zero. To count them from one subtract 1 from each value
        print("Type the row: ")
        row = int(input())
        print("Type the column: ")
        col = int(input())
        return row, col










