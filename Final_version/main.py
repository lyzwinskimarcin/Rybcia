from game_manager import GameManager

# Pycharm parameters are not yet set in this file, to set them go to pygame_visualiser
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1200
HEXAGON_SIZE = 70  # side length
N_ROWS = 7
N_COLS = 10
PENGUINS_NUMBER = 4

VISUALISATION_TYPE = "pygame"
CONTROL_PLAYER_1 = "AI"
CONTROL_PLAYER_2 = "pygame"

player_1_C = 0.6
player_1_vis_threshold = 10
player_1_draw_value = 0.3
player_1_iterations = 30000


player_2_C = 0.6
player_2_vis_threshold = 7
player_2_draw_value = 0.4
player_2_iterations = 100000



def main():
    game_manager = GameManager(N_ROWS, N_COLS, VISUALISATION_TYPE, CONTROL_PLAYER_1, CONTROL_PLAYER_2, PENGUINS_NUMBER)

    player_1_mcts = game_manager.player_1.mcts
    # player_2_mcts = game_manager.player_2.mcts

    player_1_mcts.C = player_1_C
    player_1_mcts.vis_threshold = player_1_vis_threshold
    player_1_mcts.draw_value = player_1_draw_value
    player_1_mcts.iterations = player_1_iterations

    # player_2_mcts.C = player_2_C
    # player_2_mcts.vis_threshold = player_2_vis_threshold
    # player_2_mcts.draw_value = player_2_draw_value
    # player_2_mcts.iterations = player_2_iterations

    game_manager.game()


main()

