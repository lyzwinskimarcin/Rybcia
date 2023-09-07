from board import Board
from Pygame_visualisation.pygame_visualiser import PygameVisualiser
from player import Player
import numpy as np

# Setup
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length
N_ROWS = 7
N_COLS = 10
PENGUINS_NUMBER = 2

VISUALISATION_TYPE = "pygame"
CONTROL_PLAYER_1 = "pygame"
CONTROL_PLAYER_2 = "pygame"


class GameManager:
    def __init__(self, n_rows, n_cols, visualisation_type, control_player_1, control_player_2, penguin_number):
        self.board = Board(n_rows, n_cols)
        if visualisation_type == "pygame":
            self.pygame_visualiser = PygameVisualiser(self.board)
        self.visualisation_type = visualisation_type
        self.player_1 = Player(1, self, control_player_1)
        self.player_2 = Player(2, self, control_player_2)
        self.penguin_number = penguin_number

    def visualise(self):
        if self.visualisation_type == "console":
            # Console visualisation
            print("Fish board")
            self.board.print_board(self.board.fish_board)
            print("Player board")
            self.board.print_board(self.board.player_board)
            print("Available tiles board")
            self.board.print_board(self.board.available_tiles_board)
        elif self.visualisation_type == "pygame":
            # Pygame visualisation, needs to be set up
            player_1_fish = self.board.player_1_fish
            player_1_tiles = self.board.player_1_tiles
            player_2_fish = self.board.player_2_fish
            player_2_tiles = self.board.player_2_tiles
            self.pygame_visualiser.draw_board(player_1_fish, player_1_tiles, player_2_fish, player_2_tiles)

    # METHODS FOR MAKING MOVES

    def get_penguin_pos(self, player):
        valid_positions = self.board.get_penguins_positions(player.player_number)
        pos = player.get_player_pos(self.board)
        if pos not in valid_positions:
            print(f"There is no penguin on this field: {pos}")
            pos = self.get_penguin_pos(player)
        return pos

    def get_target_pos(self, player, penguin_pos):
        valid_moves = self.board.check_valid_moves(penguin_pos)
        pos = player.get_player_pos(self.board)
        if pos not in valid_moves:
            print(f"You cannot move the selected penguin there on this field: {pos}")
            pos = self.get_target_pos(player, penguin_pos)
        return pos

    def turn(self, player):
        penguin_pos = self.get_penguin_pos(player)
        target_pos = self.get_target_pos(player, penguin_pos)
        self.board.board_move(penguin_pos, target_pos)

    # STARTING PHASE
    def put_penguin(self, player_turn):
        if player_turn == 1:
            pos = self.player_1.get_player_pos(self.board)
            try:
                self.board.choose_starting_position(pos)
            except ValueError:
                print(f"Invalid starting position: {pos}. Please try again.")
                self.put_penguin(player_turn)
        elif player_turn == 2:
            pos = self.player_2.get_player_pos(self.board)
            try:
                self.board.choose_starting_position(pos)
            except ValueError:
                print(f"Invalid starting position: {pos}. Please try again.")
                self.put_penguin(player_turn)

    def starting_phase(self, penguin_number):
        while penguin_number > 0:
            self.visualise()
            self.put_penguin(self.board.player_turn)
            penguin_number -= 1
            if self.visualisation_type == "pygame":
                self.pygame_visualiser.handle_QUIT()




    # MAIN GAME LOOP

    def game(self):
        # Starting phase
        self.starting_phase(self.penguin_number*2)  # Times two because it's per player
        self.visualise()
        # Middle game
        running = True
        while running:
            self.visualise()
            if self.board.is_game_over():
                break
            if self.board.player_turn == 1:
                available_moves = []
                penguins_positions = self.board.get_penguins_positions(1)
                for penguin_pos in penguins_positions:
                    available_moves.extend(self.board.check_valid_moves(penguin_pos))
                if len(available_moves) > 0:
                    self.turn(self.player_1)
                else:
                    self.board.player_turn = 2 if self.board.player_turn == 1 else 1
            elif self.board.player_turn == 2:
                available_moves = []
                penguins_positions = self.board.get_penguins_positions(2)
                for penguin_pos in penguins_positions:
                    available_moves.extend(self.board.check_valid_moves(penguin_pos))
                if len(available_moves) > 0:
                    self.turn(self.player_2)
                else:
                    self.board.player_turn = 2 if self.board.player_turn == 1 else 1
        self.board.game_over()













