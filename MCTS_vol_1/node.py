

class Node:
    def __init__(self, parent, move, current_player, fish_board, player_board, available_tiles_board):
        self.vis = 0
        self.val = 0

        self.fish_board = fish_board
        self.player_board = player_board
        self.available_tiles_board = available_tiles_board

        self.parent = parent
        self.children = dict()

        self.move = move
        self.current_player = current_player

        self.is_terminal = False   # needs to be checked
        self.is_expandable = True

    def create_child(self, move, current_player, fish_board, player_board, available_tiles_board):
        node = Node(self, move, current_player, fish_board, player_board, available_tiles_board)
        self.children[move] = node
        return node   # is that necessary?

    def single_run(self):
        if self.is_terminal:
            self.backporpagate()



