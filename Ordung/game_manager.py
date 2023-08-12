from Visualisation.game_visualiser import GameVisualiser
from game_logic import GameLogic
from player import Player


class GameManager:
    def __init__(self, visualisation_type, control_type, n_rows, n_cols):
        self.visualisation_type = visualisation_type
        # Initialization
        self.gameLogic = GameLogic(n_rows, n_cols)
        self.player_1 = Player(1, visualisation_type, control_type)
        self.player_2 = Player(2, visualisation_type, control_type)
        if visualisation_type == "pygame":
            self.pygameVisualiser = GameVisualiser(self.gameLogic.board)
            self.player_1.set_pygameVisualiser(self.pygameVisualiser)
            self.player_2.set_pygameVisualiser(self.pygameVisualiser)

    def visualise(self):
        if self.visualisation_type == "console":
            # Console visualisation
            print("Fish board")
            self.gameLogic.board.print_board(self.gameLogic.board.fish_board)
            print("Player board")
            self.gameLogic.board.print_board(self.gameLogic.board.player_board)
            print("Available tiles board")
            self.gameLogic.board.print_board(self.gameLogic.board.available_tiles_board)
        elif self.visualisation_type == "pygame":
            # Pygame visualisation, needs to be set up
            self.pygameVisualiser.draw_grid()

    def choose_starting_positions(self, penguin_number):
        while penguin_number >= 0:
            self.visualise()
            valid_starting_moves = self.gameLogic.board.get_valid_starting_positions()
            row, col = self.player_1.get_player_move(is_starting_pos=True, valid_starting_moves=valid_starting_moves)
            self.gameLogic.choose_starting_position(self.player_1.player_number, row, col)
            self.visualise()
            valid_starting_moves = self.gameLogic.board.get_valid_starting_positions()
            row, col = self.player_2.get_player_move(is_starting_pos=True, valid_starting_moves=valid_starting_moves)
            self.gameLogic.choose_starting_position(self.player_2.player_number, row, col)

            penguin_number -= 2

    def game(self):
        while True:
            if self.gameLogic.is_game_over():
                break
            self.visualise()
            self.player_move(self.player_1)
            if self.gameLogic.is_game_over():
                break
            self.visualise()
            self.player_move(self.player_2)



            if self.visualisation_type == "pygame":
                self.pygameVisualiser.handle_QUIT()

    def player_move(self, player):
        number_of_moves = 0
        valid_moves = self.gameLogic.board.check_valid_moves(player.player_number)
        print(valid_moves)
        for moves_lst in valid_moves.values():
            number_of_moves += len(moves_lst)
        if number_of_moves > 0:
            penguin_row, penguin_col = player.get_player_move()
            target_row, target_col = player.get_player_move()
            condition_player = self.gameLogic.board.player_board[penguin_row][penguin_col] == player.player_number
            valid_moves_pos = self.gameLogic.board.check_valid_moves_helper((penguin_row, penguin_col))
            if [target_row, target_col] in valid_moves_pos and condition_player:
                self.gameLogic.make_move(player.player_number, penguin_row, penguin_col, target_row, target_col)
            else:
                self.player_move(player)










