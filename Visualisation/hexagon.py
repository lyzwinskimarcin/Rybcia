import pygame
import math


class Hexagon:
    def __init__(self, row, col, center_x, center_y, fish, window, hexagon_size):
        self.row = row
        self.col = col
        self.fish = fish
        self.is_visible = True
        self.player_number = 0
        self.center_x = center_x
        self.center_y = center_y
        self.window = window
        self.vertices = self.set_vertices(hexagon_size)

    def set_vertices(self, hexagon_size):
        vertices = []
        for i in range(6):
            angle_deg = 60 * i - 30  # Note: This angle is in degrees
            angle_rad = math.pi / 180 * angle_deg  # Convert to radians
            x = self.center_x + (hexagon_size - 3) * math.cos(angle_rad) # minus 3 in order to see borders
            y = self.center_y + (hexagon_size - 3) * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices

    def update_hexagon(self, board):
        if self.is_visible:
            is_available = board.available_tiles_board[self.row][self.col] == 1
            player_number = board.player_board[self.row][self.col]
            if not is_available and not player_number != 0:
                self.is_visible = False
            elif not is_available and player_number != 0:
                self.player_number = player_number

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
        # debug_color = (0, 255, 0)
        # pygame.draw.circle(self.window, debug_color, (self.center_x, self.center_y), 5)