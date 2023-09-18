from try_num_4.board import Board
from hexagon_editor_version import Hexagon
import pygame
import math
import pickle

WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length


class Editor:
    def __init__(self, board):
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.board = board
        self.grid = self.create_grid()
        self.button_pos = (WINDOW_WIDTH - 120, WINDOW_HEIGHT - 120)
        self.button_radius = 50

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

    def draw_board(self):
        self.draw_grid()
        self.draw_button()
        pygame.display.flip()

    def draw_button(self):
        color = (0, 50, 60)
        x = self.button_pos[0]
        y = self.button_pos[1]
        pygame.draw.circle(self.window, color, (x, y), self.button_radius)

    def is_button_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.button_pos[0]) ** 2 + (pos[1] - self.button_pos[1]) ** 2)
        if distance <= self.button_radius:
            self.save_board()


    def save_board(self):
        with open("board.pkl", "wb") as f:
            pickle.dump(self.board, f)
        exit()

    def draw_grid(self):
        self.window.fill((0, 0, 0))
        for row_lst in self.grid:
            for hexagon in row_lst:
                hexagon.update_hexagon(self.board)
                hexagon.draw_hexagon()

    def handle_QUIT(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # The user clicked the close button
                pygame.quit()

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
                    self.is_button_clicked(event.pos)
                    pos = self.check_which_hexagon(event.pos)
                    waiting_on_click = False
        if pos is None:
            raise ValueError(f"Error: There was a problem with getting the move from the mouse click.")
        else:
            return pos



