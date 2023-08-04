import numpy as np
import pygame
from board import Board
from game_logic import GameLogic
from Visualisation.game_visualiser import GameVisualiser




WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length
N_ROWS = 8
N_COLS = 10
VISUALISATION_ON = True


def main():
    # Initialize board and game logic
    gameLogic = GameLogic(N_ROWS, N_COLS)

    # Setup pygame if needed
    if VISUALISATION_ON:
        # pygame setup method from game visualiser
        gameVisualiser = GameVisualiser(gameLogic.board)


    # Choosing starting positions
    if VISUALISATION_ON:
        # Get positions from the clicks
        row, col = gameVisualiser.handle_events()
        gameLogic
    else:
        # Get positions from the console or other
        pass

    # Use positions to place penguins


    # MAIN LOOP
    choose_positions = True
    player_turn = 1
    running = True
    while running:
        if choose_positions:
            # Choosing starting positions
            if VISUALISATION_ON:
                # Get positions from the clicks
                row, col = gameVisualiser.handle_events()
                gameLogic.choose_starting_position(player_turn, row, col)
            else:
                # Get positions from the console or other
                pass
            if choose_positions and player_turn == 2:
                choose_positions = False
                player_turn = 1
            else:
                player_turn = 2

        else:
            if gameLogic.is_game_over():
                break
            # Player 1 turn
            if VISUALISATION_ON:
                # Get positions from the clicks
                row, col = gameVisualiser.handle_events()
                gameVisualiser.update_visualisation()
                gameVisualiser.draw_grid()
            else:
                # Get positions from the console or other
                pass


main()










