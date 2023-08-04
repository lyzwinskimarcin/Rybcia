import numpy as np

def check_valid_moves_helper(self, position):
    """Helper function checking for valid moves for the given position and not for the player"""
    valid_moves_for_position = []
    # List of possible directions to move in (up, down, left, right, up-left, up-right for even rows and down-left, down-right for odd rows)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)] if position[0] % 2 == 0 else [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (1, 1)]
    # Check all tiles in each direction
    for dx, dy in directions:
        new_x, new_y = position[0] + dx, position[1] + dy
        # Check if the new position is within the board and is available
        while 0 <= new_x < self.n_rows and 0 <= new_y < self.n_cols and self.available_tiles_board[new_x][new_y] == 1:
            valid_moves_for_position.append([new_x, new_y])
            new_x, new_y = new_x + dx, new_y + dy
    return valid_moves_for_position



# Create a 2D numpy array
some_numbers = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Define a position
position = [1, 2]
d_x = 1
d_y = -1


# Assign a new value to the element at the given position
some_numbers[position] = 7

print(some_numbers)
print(position + [d_x, d_x])