
choose_start_positions()

running = True
while running:
    is_game_over()
    move = get_player_move()
    player_1_move(move)
    is_game_over()
    move = get_AI_move()
    player_2_move(move)







