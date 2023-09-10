import pygame
import math
from .hexagon import Hexagon
import os

# Set the position of the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (700, 100)


WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1200
HEXAGON_SIZE = 70  # side length


class PygameVisualiser:
    def __init__(self, board):
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
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
                hexagon.update_hexagon(self.board)
                hexagon.draw_hexagon()

    def display_score(self, player_1_fish, player_1_tiles, player_2_fish, player_2_tiles):
        line_height = 30
        x_offset = 250
        y_offset = 10
        x = WINDOW_WIDTH - x_offset
        y = y_offset

        player_1_fish_text = f"Player 1 fish: {player_1_fish}"
        player_1_tiles_text = f"Player 1 tiles: {player_1_tiles}"
        player_2_fish_text = f"Player 2 fish: {player_2_fish}"
        player_2_tiles_text = f"Player 2 tiles: {player_2_tiles}"
        lines = [player_1_fish_text, player_1_tiles_text, player_2_fish_text, player_2_tiles_text]
        for line in lines:
            text_surface = self.my_font.render(line, False, (255, 255, 255))
            self.window.blit(text_surface, (x, y))
            y += line_height

    def draw_board(self, player_1_fish, player_1_tiles, player_2_fish, player_2_tiles):
        self.draw_grid()
        self.display_score(player_1_fish, player_1_tiles, player_2_fish, player_2_tiles)
        pygame.display.flip()

    def handle_QUIT(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # The user clicked the close button
                pygame.quit()
            # THIS IS USELESS RIGHT?
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     row, col = self.check_which_hexagon(event.pos)
            #     return row, col

    def check_which_hexagon(self, pos):
        click_radius = 0.85 * HEXAGON_SIZE  # inside circle radius approximation
        for row_lst in self.grid:
            for hexagon in row_lst:
                distance = math.sqrt((pos[0] - hexagon.center_x) ** 2 + (pos[1] - hexagon.center_y) ** 2)
                if distance <= click_radius:
                    hex_pos = (hexagon.row, hexagon.col)
                    return hex_pos

    def get_mouse_move(self):
        waiting_on_click = True
        while waiting_on_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # The user clicked the close button
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.check_which_hexagon(event.pos)
                    waiting_on_click = False
        if pos == None:
            raise ValueError(f"Error: There was a problem with getting the move from the mouse click.")
        else:
            return pos



