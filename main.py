import numpy as np
import pygame
from board import Board
from game_logic import GameLogic
from game_visualisation import Hexagon, create_grid, draw_grid, update_hexagon

WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length
N_ROWS = 8
N_COLS = 10


def main():

    # Initialize Pygame
    pygame.init()
    # Create a window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    board = Board(N_ROWS, N_COLS)
    grid = create_grid(N_ROWS, N_COLS, board, window)
    draw_grid(grid)
    # Update the display
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # The user clicked the close button
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                update_hexagon(event.pos, grid)
                window.fill((0, 0, 0))
                draw_grid(grid)
                pygame.display.flip()


main()








