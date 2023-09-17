from mcts_vol_4.mcts_vol_4 import MCTS
from board import Board

PLAYER_1_C = 1.0
PLAYER_2_C = 1.0


class Player:
    def __init__(self, player_number, game_manager, control_type="console"):
        """Set "console" to control the game from console, "pygame" to control through pygame.
                You can set control_type to "AI" to play against AI"""
        self.visits = 0  # For debugging
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
            self.mcts = MCTS(game_manager.board.n_rows, game_manager.board.n_cols, game_manager.number_of_penguins, iterations=10000, C_value=C)

    def get_console_pos(self):
        # Rows and columns counted from zero. To count them from one subtract 1 from each value
        print("Type the row: ")
        row = int(input())
        print("Type the column: ")
        col = int(input())
        pos = (row, col)
        return pos

    def get_starting_move(self, board):
        if self.control_type == "pygame":
            move = self.pygame_visualiser.get_mouse_move()
        elif self.control_type == "console":
            move = self.get_console_pos()
        elif self.control_type == "AI":
            # We'll see how mcts is implemented
            move = self.mcts.get_move(board)
        return move

    def get_player_move(self, board):
        if board.is_starting_phase:
            move = self.get_starting_move(board)
        else:
            if self.control_type == "pygame":
                move = self.get_pygame_move(board)
            elif self.control_type == "console":
                move = self.get_console_move(board)
            elif self.control_type == "AI":
                # We'll see how mcts is implemented
                move = self.get_mcts_move(board)
        return move

    # METHODS FOR MOVES DEPENDING ON PLAYER CONTROL

    def get_pygame_move(self, board):
        penguin_pos = self.pygame_visualiser.get_mouse_move()
        valid_penguin_pos = board.get_penguins_positions(board.player_turn)
        if penguin_pos not in valid_penguin_pos:
            print(f"There is no penguin at {penguin_pos}")
            penguin_pos = self.pygame_visualiser.get_mouse_move()
        target_pos = self.pygame_visualiser.get_mouse_move()
        valid_moves = board.get_valid_moves()
        move = (penguin_pos, target_pos)
        if move not in valid_moves:
            print(f"You cannot move penguin {penguin_pos} to {target_pos}")
            move = self.get_pygame_move(board)
        return move

    def get_console_move(self, board):
        penguin_pos = self.get_console_pos()
        valid_penguin_pos = board.get_penguins_positions(board.player_turn)
        if penguin_pos not in valid_penguin_pos:
            print(f"There is no penguin at {penguin_pos}")
            penguin_pos = self.get_pygame_move(board)
        target_pos = self.get_console_pos()
        valid_moves = board.get_valid_moves()
        move = (penguin_pos, target_pos)
        if move not in valid_moves:
            print(f"You cannot move penguin {penguin_pos} to {target_pos}")
            move = self.get_console_move(board)
        return move

    def get_mcts_move(self, board):
        move = self.mcts.get_move(board)
        valid_moves = board.get_valid_moves()
        if move not in valid_moves:
            print(f"Invalid mcts move given: {move}")
            move = self.mcts.get_move(board)
        return move


