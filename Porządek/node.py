

class Node:
    def __init__(self, fish_board, player_board, available_tiles_board):
        self.fish_board = fish_board
        self.player_board = player_board
        self.available_tiles_board = available_tiles_board
        self.val = 0
        self.vis = 1  # we'll see about that
        self.children = {}

    def create_child(self, move, board):
        node = Node(board.fish_board, board.player_board, board.available_tiles_board)
        self.children[move] = node
        # Not yet sure if needed but:
        return node







