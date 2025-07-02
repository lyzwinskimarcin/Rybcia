from game_manager import GameManager


N_ROWS = 7
N_COLS = 10
PENGUINS_NUMBER = 4

# Visualisation parameters like window size can be set in pygame_visualiser.py file
VISUALISATION_TYPE = "pygame"  # Possible "pygame", "console" or any other string will result in no visualisation

# Possible "pygame" if matches visualisation type, "console" regardless of visualisation or "AI"for mcts based opponent
CONTROL_PLAYER_1 = "pygame"
CONTROL_PLAYER_2 = "AI"

player_1_C = 0.8
player_1_vis_threshold = 10
player_1_draw_value = 0.4
player_1_iterations = 10000


player_2_C = 0.8
player_2_vis_threshold = 10
player_2_draw_value = 0.4
player_2_iterations = 5000




def main():
    game_manager = GameManager(N_ROWS, N_COLS, VISUALISATION_TYPE, CONTROL_PLAYER_1, CONTROL_PLAYER_2, PENGUINS_NUMBER)

    # Code below allows to overwrite mcts parameters

    # player_1_mcts = game_manager.player_1.mcts
    player_2_mcts = game_manager.player_2.mcts

    # player_1_mcts.C = player_1_C
    # player_1_mcts.vis_threshold = player_1_vis_threshold
    # player_1_mcts.draw_value = player_1_draw_value
    # player_1_mcts.iterations = player_1_iterations

    player_2_mcts.C = player_2_C
    player_2_mcts.vis_threshold = player_2_vis_threshold
    player_2_mcts.draw_value = player_2_draw_value
    player_2_mcts.iterations = player_2_iterations

    # Running game
    game_manager.game()


main()

