import numpy as np
import pygame
from board import Board
from game_logic import GameLogic
from Visualisation.game_visualiser import GameVisualiser


WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length
N_ROWS = 5
N_COLS = 5
PENGUINS_NUMBER = 2
VISUALISATION_ON = True

def visualise(condition, board):
    if condition:
        print("Fish board")
        board.print_board(board.fish_board)
        print("Player board")
        board.print_board(board.player_board)
        print("Available tiles board")
        board.print_board(board.available_tiles_board)

def change_turn(player_turn):
    return player_turn % 2 + 1


def main():
    # Initialize board and game logic
    gameLogic = GameLogic(N_ROWS, N_COLS)
    player_turn = 1
    # Set starting positions for the players
    choose_positions_phase = True
    running = True
    while running:
        # Firstly choose the starting positions for the penguins
        if choose_positions_phase:
            # Visualise the board
            visualise(VISUALISATION_ON, gameLogic.board)

            # Get input for the move
            row, col = gameLogic.get_move_input()
            gameLogic.choose_starting_position(player_turn, row, col)
            # Change turn
            player_turn = change_turn(player_turn)

            # Repeat for the second player (it's not looped so that it's easy to implement AI)
            visualise(VISUALISATION_ON, gameLogic.board)
            row, col = gameLogic.get_move_input()
            gameLogic.choose_starting_position(player_turn, row, col)
            player_turn = change_turn(player_turn)

            # Check if all the penguins are already located on the board
            penguin_number = gameLogic.board.get_penguin_number()
            if penguin_number == PENGUINS_NUMBER:
                choose_positions_phase = False
        else:
            # The main part of the game
            visualise(VISUALISATION_ON, gameLogic.board)
            break


main()
