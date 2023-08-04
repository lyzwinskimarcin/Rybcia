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
VISUALISATION_SETTING = "Pygame"


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


def change_turn(player_turn):
    return player_turn % 2 + 1


def main():
    # Initialize board and game logic
    gameLogic = GameLogic(N_ROWS, N_COLS)
    player_turn = 1

    # Setup pygame if needed
    if VISUALISATION_SETTING == "Pygame":
        # pygame setup method from game visualiser
        gameVisualiser = GameVisualiser(gameLogic.board)
    else:
        gameVisualiser = None

    # Set starting positions for the players
    choose_positions_phase = True
    running = True
    while running:
        # Firstly choose the starting positions for the penguins
        if choose_positions_phase:
            # Visualise the board
            visualise(VISUALISATION_SETTING, gameLogic.board, gameVisualiser)

            # Get input for the move
            row, col = gameVisualiser.get_mouse_move()
            gameLogic.choose_starting_position(player_turn, row, col)
            # Change turn
            player_turn = change_turn(player_turn)

            # Repeat for the second player (it's not looped so that it's easy to implement AI)
            visualise(VISUALISATION_SETTING, gameLogic.board, gameVisualiser)
            row, col = gameVisualiser.get_mouse_move()
            gameLogic.choose_starting_position(player_turn, row, col)
            player_turn = change_turn(player_turn)

            # Check if all the penguins are already located on the board
            penguin_number = gameLogic.board.get_penguin_number()
            if penguin_number == PENGUINS_NUMBER:
                choose_positions_phase = False
        else:
            # The main part of the game
            visualise(VISUALISATION_SETTING, gameLogic.board, gameVisualiser)
            if gameLogic.is_game_over():
                break
            # Player 1 move
            penguin_row, penguin_col = gameVisualiser.get_mouse_move()
            target_row, target_col = gameVisualiser.get_mouse_move()
            gameLogic.make_move(player_turn, penguin_row, penguin_col, target_row, target_col)
            player_turn = change_turn(player_turn)

            visualise(VISUALISATION_SETTING, gameLogic.board, gameVisualiser)

            if gameLogic.is_game_over():
                break
            # Player 2 move
            penguin_row, penguin_col = gameVisualiser.get_mouse_move()
            target_row, target_col = gameVisualiser.get_mouse_move()
            gameLogic.make_move(player_turn, penguin_row, penguin_col, target_row, target_col)
            player_turn = change_turn(player_turn)

            visualise(VISUALISATION_SETTING, gameLogic.board, gameVisualiser)
            if VISUALISATION_SETTING == "Pygame":
                gameVisualiser.handle_QUIT()


main()
