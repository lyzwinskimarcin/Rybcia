from visual_board_editor.editor import Editor
from try_num_4.board import Board


class EditorEngine:

    def create_board(self):
        n_rows = int(input("Provide row number: "))
        n_cols = int(input("Provide column number: "))
        number_of_penguins = int(input("Provide number of penguins: "))
        board = Board(n_rows, n_cols, number_of_penguins)
        self.editor = Editor(board)

    def main_loop(self):
        self.create_board()
        running = True
        while running:
            self.editor.draw_board()
            pos = self.editor.get_mouse_move()
            if self.editor.board.fish_board[pos] < 3:
                self.editor.board.fish_board[pos] += 1
            else:
                self.editor.board.fish_board[pos] = 1



editor_engine = EditorEngine()
editor_engine.main_loop()
