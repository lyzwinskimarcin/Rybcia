import pygame
import math
from board import Board

WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70 #side length
N_ROWS = 8
N_COLS = 10


class Hexagon:
    def __init__(self, row, col, center_x, center_y, board, window):
        self.row = row
        self.col = col
        self.fish = board.fish_board[row][col]
        self.player_number = board.player_board[row][col]
        self.is_visible = True
        self.center_x = center_x
        self.center_y = center_y
        self.window = window
        self.vertices = self.set_vertices()

    def set_vertices(self):
        vertices = []
        for i in range(6):
            angle_deg = 60 * i - 30  # Note: This angle is in degrees
            angle_rad = math.pi / 180 * angle_deg  # Convert to radians
            x = self.center_x + (HEXAGON_SIZE - 3) * math.cos(angle_rad) # minus 3 in order to see borders
            y = self.center_y + (HEXAGON_SIZE - 3) * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices

    def draw_hexagon(self):
        if self.is_visible:
            pygame.draw.polygon(self.window, (255, 255, 255), self.vertices)
            self.draw_fish_number(self.center_x, self.center_y)
            if self.player_number != 0:
                self.draw_player()

    def draw_player(self):
        player_offset = 10
        player_size = 4
        color_1 = (0, 255, 0)
        color_2 = (0, 0, 255)
        color = color_1 if self.player_number == 1 else color_2
        pygame.draw.circle(self.window, color, (self.center_x, self.center_y - player_offset), player_size)

    def draw_fish_number(self, center_x, center_y):
        rect_color = (255, 0, 0)
        rect_width = 4
        rect_height = 20
        rect_distance = 10
        rect_offset = 10

        def draw_fish_rect(_rect_x, _rect_y):
            rect = pygame.Rect(_rect_x, _rect_y, rect_width, rect_height)
            pygame.draw.rect(self.window, rect_color, rect)

        if self.fish == 1:
            rect_x = center_x - (rect_width/2)
            rect_y = center_y + rect_offset
            draw_fish_rect(rect_x, rect_y)
        elif self.fish == 2:
            rect_x = center_x - (rect_width / 2) - (rect_distance / 2)
            rect_y = center_y + rect_offset
            draw_fish_rect(rect_x, rect_y)
            rect_x += rect_distance
            draw_fish_rect(rect_x, rect_y)
        elif self.fish == 3:
            rect_x = center_x - (rect_width / 2) - rect_distance
            rect_y = center_y + rect_offset
            draw_fish_rect(rect_x, rect_y)
            for _ in range(2):
                rect_x += rect_distance
                draw_fish_rect(rect_x, rect_y)

        # Debugging (draws the center point of the hexagon)
        debug_color = (0, 255, 0)
        pygame.draw.circle(self.window, debug_color, (self.center_x, self.center_y), 5)


def create_grid(n_rows, n_cols, board, window):
    grid = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    center_x = HEXAGON_SIZE
    center_y = HEXAGON_SIZE
    d = HEXAGON_SIZE * math.sqrt(3)  # distance to the next hexagon center position
    for row in range(n_rows):
        for col in range(n_cols):
            hexagon = Hexagon(row, col, center_x, center_y, board, window)
            center_x += d
            grid[row][col] = hexagon
        if row % 2 == 0:
            center_x = HEXAGON_SIZE + d/2
        else:
            center_x = HEXAGON_SIZE

        center_y += 1.5 * HEXAGON_SIZE
    return grid


def draw_grid(grid):
    for row_lst in grid:
        for hexagon in row_lst:
            hexagon.draw_hexagon()


def check_which_hexagon(pos, grid):
    click_radius = 0.85 * HEXAGON_SIZE # inside circle radius approximation
    for row_lst in grid:
        for hexagon in row_lst:
            distance = math.sqrt((pos[0] - hexagon.center_x)**2 + (pos[1] - hexagon.center_y)**2)
            if distance <= click_radius:
                return hexagon


def update_hexagon(pos, grid):
    hexagon = check_which_hexagon(pos, grid)
    if hexagon != None:
        return hexagon.row, hexagon.col



# def update_hexagon(pos, grid):
#     row, col = check_which_hexagon(pos, grid)
#     if row != None:
#         hexagon = grid[row][col]
#         hexagon.fish = 1
#         grid[row][col] = hexagon


def main():

    # Initialize Pygame
    pygame.init()
    # Create a window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    board = Board(N_ROWS, N_COLS)
    grid = create_grid(N_ROWS, N_COLS, board, window)
    draw_grid(grid)

    board.choose_starting_position(2, 3, 1)
    board.choose_starting_position(7, 9, 2)

    # Update the display
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # The user clicked the close button
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = update_hexagon(event.pos, grid)
                board.fish_board[row][col] = 1
                window.fill((0, 0, 0))
                draw_grid(grid)
                pygame.display.flip()
                board.print_board(board.fish_board)


main()

