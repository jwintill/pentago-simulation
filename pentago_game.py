import numpy as np
import pygame
import sys
from pentago import PentagoGame
# Define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (69, 14, 4)
GRID_SIZE = 3  # Size of each subgrid
NUM_WIN = 5  # number of pieces you need in a row to win

# Initialize Pygame
pygame.init()

# Set up Pygame window and other configurations
WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Pentago")

# Set up the game
pentago_game = PentagoGame()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // (WINDOW_SIZE[1] // 6)
            col = mouse_pos[0] // (WINDOW_SIZE[0] // 6)

            if event.button == 1:  # Left-click
                move = (row, col)
                pentago_game.make_move(pentago_game.current_player, move)

        elif event.type == pygame.KEYDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // (WINDOW_SIZE[1] // 6)
            col = mouse_pos[0] // (WINDOW_SIZE[0] // 6)
            if event.key == pygame.K_r:  # Press 'r' key to rotate right
                quadrant = (row // 3) * 2 + (col // 3)
                direction = 'CC'
                if (not pentago_game.hasRotated):
                    pentago_game.rotate_grid(quadrant, direction)

            elif event.key == pygame.K_l:  # Press 'l' key to rotate left
                quadrant = (row // 3) * 2 + (col // 3)
                direction = 'C'
                if (not pentago_game.hasRotated):
                    pentago_game.rotate_grid(quadrant, direction)

            # Check for a winner after every move
            winner = pentago_game.check_winner()
            if winner != 0:
                print(f"Player {winner} wins!")
                pygame.quit()
                sys.exit()

            # Switch to the next player
            if (pentago_game.hasPlaced and pentago_game.hasRotated):
                pentago_game.current_player *= -1
                pentago_game.hasPlaced = False
                pentago_game.hasRotated = False

    # Draw the current game state on the Pygame window
    screen.fill(BACKGROUND)  # Clear the screen

    # Draw the game board
    for row in range(6):
        for col in range(6):
            pygame.draw.circle(screen, (BACKGROUND[0]-10, BACKGROUND[1]-10, BACKGROUND[2]), (col * (WINDOW_SIZE[0] // 6) + WINDOW_SIZE[0] // 12,
                                                  row * (WINDOW_SIZE[1] // 6) + WINDOW_SIZE[1] // 12),
                                   min(WINDOW_SIZE[0] // 15, WINDOW_SIZE[1] // 15))

    # Draw game pieces
    for row in range(6):
        for col in range(6):
            if pentago_game.board[row, col] == 1:
                pygame.draw.circle(screen, BLACK, (col * (WINDOW_SIZE[0] // 6) + WINDOW_SIZE[0] // 12,
                                                  row * (WINDOW_SIZE[1] // 6) + WINDOW_SIZE[1] // 12),
                                   min(WINDOW_SIZE[0] // 15, WINDOW_SIZE[1] // 15))
            elif pentago_game.board[row, col] == -1:
                pygame.draw.circle(screen, WHITE, (col * (WINDOW_SIZE[0] // 6) + WINDOW_SIZE[0] // 12,
                                                  row * (WINDOW_SIZE[1] // 6) + WINDOW_SIZE[1] // 12),
                                   min(WINDOW_SIZE[0] // 15, WINDOW_SIZE[1] // 15))

    # Draw rotation indicator lines
    pygame.draw.line(screen, (WHITE[0]-50, WHITE[1]-50, WHITE[2]-60), (0, WINDOW_SIZE[1] // 2),
                     (WINDOW_SIZE[0], (WINDOW_SIZE[1] // 2)), (WINDOW_SIZE[0] // 60))
    pygame.draw.line(screen, (WHITE[0]-50, WHITE[1]-50, WHITE[2]-60), (WINDOW_SIZE[0] // 2, 0),
                     (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]), (WINDOW_SIZE[0] // 60))


    # Draw player turn indicator
    player_turn_text = f"Player {1 if pentago_game.current_player == 1 else 2}'s turn"
    font = pygame.font.Font(None, 36)
    text = font.render(player_turn_text, True, BLACK)
    screen.blit(text, (10, 10))

    # Update the Pygame display
    pygame.display.flip()
