from try_num_4.game_manager import GameManager


N_ROWS = 5
N_COLS = 7
PENGUINS_NUMBER = 4

VISUALISATION_TYPE = "pygame"
CONTROL_PLAYER_1 = "AI"
CONTROL_PLAYER_2 = "pygame"



class Setup:
    def __init__(self, n_rows, n_cols, number_of_penguins, num_of_iterations):
        self.game_manager = GameManager(n_rows, n_cols, None, "AI", "AI", number_of_penguins)


    def

