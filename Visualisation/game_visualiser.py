import pygame
import math
from Visualisation.hexagon import Hexagon


WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length


class GameVisualiser:
    def __init__(self, board):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.board = board
        self.grid = self.create_grid()

    def create_grid(self):
        grid = [[None for _ in range(self.board.n_cols)] for _ in range(self.board.n_rows)]
        center_x = HEXAGON_SIZE
        center_y = HEXAGON_SIZE
        d = HEXAGON_SIZE * math.sqrt(3)  # distance to the next hexagon center position
        for row in range(self.board.n_rows):
            for col in range(self.board.n_cols):
                fish = self.board.fish_board[row][col]
                hexagon = Hexagon(row, col, center_x, center_y, fish, self.window, HEXAGON_SIZE)
                center_x += d
                grid[row][col] = hexagon
            if row % 2 == 0:
                center_x = HEXAGON_SIZE + d / 2
            else:
                center_x = HEXAGON_SIZE

            center_y += 1.5 * HEXAGON_SIZE
        return grid

    def draw_grid(self):
        self.window.fill((0, 0, 0))
        for row_lst in self.grid:
            for hexagon in row_lst:
                hexagon.draw_hexagon()
        pygame.display.flip()

    def update_visualisation(self):
        for row_lst in self.grid:
            for hexagon in row_lst:
                hexagon.update_hexagon(self.board)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # The user clicked the close button
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = self.check_which_hexagon(event.pos)
                return row, col

    def check_which_hexagon(self, pos):
        click_radius = 0.85 * HEXAGON_SIZE  # inside circle radius approximation
        for row_lst in self.grid:
            for hexagon in row_lst:
                distance = math.sqrt((pos[0] - hexagon.center_x) ** 2 + (pos[1] - hexagon.center_y) ** 2)
                if distance <= click_radius:
                    return hexagon.row, hexagon.col

    def get_mouse_move(self):
        waiting_on_click = True
        while waiting_on_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # The user clicked the close button
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = self.check_which_hexagon(event.pos)
                    waiting_on_click = False
        if row == None or col == None:
            raise ValueError(f"Error: There was a problem with getting the move from the mouse click.")
        else:
            return row, col



