import time
from board import Board
from player import Player
from Pygame_visualisation.pygame_visualiser import PygameVisualiser


class GameManager:
    def __init__(self, n_rows, n_cols, visualisation_type, control_player_1, control_player_2, number_of_penguins):
        self.board = Board(n_rows, n_cols, number_of_penguins=number_of_penguins)
        self.number_of_penguins = number_of_penguins
        if visualisation_type == "pygame":
            self.pygame_visualiser = PygameVisualiser(self.board)
        self.visualisation_type = visualisation_type
        self.player_1 = Player(1, self, control_player_1)
        self.player_2 = Player(2, self, control_player_2)

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

    def game(self):
        start_time = time.time()
        running = True
        while running:
            if self.board.is_game_over():
                break
            self.visualise()
            if self.board.player_turn == 1:
                move = self.player_1.get_player_move(self.board)
            elif self.board.player_turn == 2:
                start_time = time.time()
                move = self.player_2.get_player_move(self.board)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time taken: {elapsed_time} seconds")
            self.board.move(move)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)

        self.visualise()
        self.board.game_over()
        self.board.print_scores()
        time.sleep(10)




