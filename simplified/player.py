from MCTS_vol_2.mcts_vol_3 import MCTS

PLAYER_1_C = 1.0
PLAYER_2_C = 1.0

class Player:
    def __init__(self, player_number, game_manager, control_type="console"):
        """Set "console" to control the game from console, "pygame" to control through pygame.
                You can set control_type to "AI" to play against AI"""
        self.visits = 0
        self.player_number = player_number
        self.visualisation_type = game_manager.visualisation_type
        self.control_type = control_type
        if control_type == "pygame":
            self.pygame_visualiser = game_manager.pygame_visualiser
        elif control_type == "AI":
            # Initialize mcts here
            if player_number == 1:
                C = PLAYER_1_C
            else:
                C = PLAYER_2_C
            self.mcts = MCTS(game_manager.board.n_rows, game_manager.board.n_cols, game_manager.penguin_number, iterations=5000, C_value=C)

    def get_console_pos(self):
        # Rows and columns counted from zero. To count them from one subtract 1 from each value
        print("Type the row: ")
        row = int(input())
        print("Type the column: ")
        col = int(input())
        pos = (row, col)
        return pos

    def get_player_pos(self, board):
        """Returns a position selected by player object. Must be used twice per full move.
        First on choosing penguin, second on selecting the target  position to move to"""
        if self.control_type == "pygame":
            pos = self.pygame_visualiser.get_mouse_move()
        elif self.control_type == "console":
            pos = self.get_console_pos()
        elif self.control_type == "AI":
            # We'll see how mcts is implemented
            pos = self.mcts.get_pos(board)
            self.visits += 1
        return pos




