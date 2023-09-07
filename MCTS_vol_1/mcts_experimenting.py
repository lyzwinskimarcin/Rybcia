from mcts import MCTS
from node import Node
from Porządek.board import Board

N_ROWS = 7
N_COLS = 10
PENGUINS_NUMBER = 2

def main():
    board = Board(N_ROWS, N_COLS)
    board.choose_starting_position(1, 3, 5)
    board.choose_starting_position(1, 4, 4)
    board.choose_starting_position(2, 1, 1)
    board.choose_starting_position(2, 6, 2)
    board.print_board(board.player_board)
    mcts = MCTS(board)
    cos = mcts.present_penguins()
    print(type(cos))

main()

