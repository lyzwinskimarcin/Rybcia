from game_manager import GameManager

# Pycharm parameters are not yet set in this file, to set them go to pygame_visualiser
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1100
HEXAGON_SIZE = 70  # side length
N_ROWS = 5
N_COLS = 7
PENGUINS_NUMBER = 2

VISUALISATION_TYPE = "pygame"
CONTROL_PLAYER_1 = "AI"
CONTROL_PLAYER_2 = "pygame"


def main():
    game_manager = GameManager(N_ROWS, N_COLS, VISUALISATION_TYPE, CONTROL_PLAYER_1, CONTROL_PLAYER_2, PENGUINS_NUMBER)
    game_manager.game()


main()
