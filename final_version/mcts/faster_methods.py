import numpy as np
from numba import jit


@jit(nopython=True)
def game_over(board):
    # Add fish that penguins are standing on at the end of the game
    player_1_positions = np.argwhere(board[1] == 1)
    positions = []
    for pos in player_1_positions:
        positions.append((pos[0], pos[1]))
    player_1_positions = positions
    for pos in player_1_positions:
        board[3][3] += board[0][pos]
    player_2_positions = np.argwhere(board[1] == 2)
    positions = []
    for pos in player_2_positions:
        positions.append((pos[0], pos[1]))
    player_2_positions = positions
    for pos in player_2_positions:
        board[3][3] += board[0][pos]


@jit(nopython=True)
def who_won(board):
    if board[3][0][3] > board[3][0][4]:
        return 1
    elif board[3][0][3] < board[3][0][4]:
        return 2
    else:
        return 0


@jit(nopython=True)
def get_valid_starting_moves(board):
    positions_of_ones = np.argwhere((board[0] == 1) & (board[2] == 1))
    positions_of_ones_set = set()
    for row, col in positions_of_ones:
        positions_of_ones_set.add((row, col))
    return positions_of_ones_set


@jit(nopython=True)
def get_valid_penguin_moves(board, n_rows, n_cols):
    valid_moves = set()
    penguins_positions = np.argwhere(board[1] == board[3][0][1])
    positions = []
    for pos in penguins_positions:
        positions.append((pos[0], pos[1]))
    for position in positions:
        # check the row to the left
        col_step = 0
        while 0 < col_step + position[1]:
            col_step -= 1
            if board[2][position[0]][position[1] + col_step] == 1:
                valid_moves.add((position, (position[0], position[1] + col_step)))
            else:
                break

        # check the row to the right
        col_step = 0
        while col_step + position[1] < n_cols - 1:
            col_step += 1
            if board[2][position[0]][position[1] + col_step] == 1:
                valid_moves.add((position, (position[0], position[1] + col_step)))
            else:
                break

        # DIAGONALS

        # check the negative diagonal to the left
        row_step = -1
        col_step = -1 if position[0] % 2 == 0 else 0
        while position[0] + row_step >= 0 and 0 <= position[1] + col_step:
            d_row = position[0] + row_step
            d_col = position[1] + col_step  # these two are only needed to make the lines shorter
            if board[2][d_row][d_col] == 1:
                valid_moves.add((position, (d_row, d_col)))
            else:
                break
            row_step -= 1
            col_step -= 1 if d_row % 2 == 0 else 0

        # check the negative diagonal to the right
        row_step = 1
        col_step = 0 if position[0] % 2 == 0 else 1
        while position[0] + row_step <= n_rows - 1 and position[1] + col_step <= n_cols - 1:
            d_row = position[0] + row_step
            d_col = position[1] + col_step  # these two are only needed to make the lines shorter
            if board[2][d_row][d_col] == 1:
                valid_moves.add((position, (d_row, d_col)))
            else:
                break
            row_step += 1
            col_step += 0 if d_row % 2 == 0 else 1

        # check the positive diagonal to the left
        row_step = 1
        col_step = -1 if position[0] % 2 == 0 else 0
        while position[0] + row_step <= n_rows - 1 and 0 <= position[1] + col_step:
            d_row = position[0] + row_step
            d_col = position[1] + col_step  # these two are only needed to make the lines shorter
            if board[2][d_row][d_col] == 1:
                valid_moves.add((position, (d_row, d_col)))
            else:
                break
            row_step += 1
            col_step -= 1 if d_row % 2 == 0 else 0

        # check the negative diagonal to the right
        row_step = -1
        col_step = 0 if position[0] % 2 == 0 else 1
        while position[0] + row_step >= 0 and position[1] + col_step <= n_cols - 1:
            d_row = position[0] + row_step
            d_col = position[1] + col_step  # these two are only needed to make the lines shorter
            if board[2][d_row][d_col] == 1:
                valid_moves.add((position, (d_row, d_col)))
            else:
                break
            row_step -= 1
            col_step += 0 if d_row % 2 == 0 else 1

    return valid_moves


@jit(nopython=True)
def starting_move(board, move):
    board[1][move] = board[3][0][1]
    board[2][move] = 0
    # Turn change
    board[3][0][1] = 3 - board[3][0][1]

    if np.count_nonzero(board[1]) == board[3][0][2]:
        board[3][0][0] = False


@jit(nopython=True)
def middle_game_move(board, move):
    penguin_pos = move[0]
    target_pos = move[1]
    if board[3][0][1] == 1:
        board[3][0][3] += board[0][penguin_pos]
        board[0][penguin_pos] = 0
        board[1][penguin_pos] = 0
        board[1][target_pos] = 1
        board[2][target_pos] = 0
    elif board[3][0][1] == 2:
        board[3][0][4] += board[0][penguin_pos]
        board[0][penguin_pos] = 0
        board[1][penguin_pos] = 0
        board[1][target_pos] = 2
        board[2][target_pos] = 0
    # Turn change
    board[3][0][1] = 3 - board[3][0][1]


@jit(nopython=True)
def find_limiting_moves(valid_moves, opponent_moves):
    # Create a list for opponent fields instead of a set
    opponent_fields = []
    for move in opponent_moves:
        if move[1] not in opponent_fields:
            opponent_fields.append(move[1])

    # Create a list for limiting moves instead of a set
    limiting_moves = []
    for move in valid_moves:
        if move[1] in opponent_fields:
            limiting_moves.append(move)

    return limiting_moves








