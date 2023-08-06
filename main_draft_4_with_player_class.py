import numpy as np
import pygame
from board import Board
from game_logic import GameLogic
from Visualisation.game_visualiser import GameVisualiser
from player import Player


WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length
N_ROWS = 5
N_COLS = 5
PENGUINS_NUMBER = 2
VISUALISATION_TYPE = "console"
CONTROL_TYPE = "console"


def visualise(vis_setting, board, gameVisualiser = None):
    if vis_setting == "Pygame":
        gameVisualiser.draw_grid()
    elif vis_setting == "Console":
        print("Fish board")
        board.print_board(board.fish_board)
        print("Player board")
        board.print_board(board.player_board)
        print("Available tiles board")
        board.print_board(board.available_tiles_board)
    else:
        pass


def main():
    # Initialize game_logic and board inside
    gameLogic = GameLogic(N_ROWS, N_COLS)
    # Setting up the players. (AI_play, how to control players)
    player_1 = Player(1, VISUALISATION_TYPE, CONTROL_TYPE)
    player_2 = Player(2, VISUALISATION_TYPE, CONTROL_TYPE)

    # If pygame is being used then setup pygame
    if VISUALISATION_TYPE == "pygame":
        gameVisualiser = GameVisualiser(gameLogic.board)
        player_1.set_gameVisualiser(gameVisualiser)
        player_2.set_gameVisualiser(gameVisualiser)

    # Choose starting positions
    row, col = player_1.get_player_move()
    gameLogic.choose_starting_position(player_1.player_number, row, col)






main()


