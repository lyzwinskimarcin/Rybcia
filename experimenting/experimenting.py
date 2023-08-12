import pygame


WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1700
score_1 = 100
score_2 = 300
current_player = 1

def draw_some_shit(window):
    color = (255, 255, 0)
    rect = pygame.Rect(300, 300, 200, 400)
    pygame.draw.rect(window, color, rect)

def draw_text(window):
    font = pygame.font.Font(None, 36)  # Choose the font and size
    score_text = f"Player 1: {score_1} - Player 2: {score_2}"
    turn_text = f"Player {current_player}'s turn"

    score_surface = font.render(score_text, True, (255, 255, 255))
    turn_surface = font.render(turn_text, True, (255, 255, 255))

    window.blit(score_surface, (1000, 10))  # Position of the score text
    window.blit(turn_surface, (10, 40))   # Position of the turn text


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    draw_some_shit(window)
    draw_text(window)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

main()





