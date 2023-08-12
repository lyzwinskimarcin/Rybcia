from game_manager import GameManager


WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
HEXAGON_SIZE = 70  # side length
N_ROWS = 7
N_COLS = 10
PENGUINS_NUMBER = 2

VISUALISATION_TYPE = "pygame"
CONTROL_TYPE = "pygame"

# VISUALISATION_TYPE = "console"
# CONTROL_TYPE = "console"


def main():
    gameManager = GameManager(VISUALISATION_TYPE, CONTROL_TYPE, N_ROWS, N_COLS)
    gameManager.choose_starting_positions(PENGUINS_NUMBER)
    gameManager.game()
    gameManager.gameLogic.game_over()


main()





