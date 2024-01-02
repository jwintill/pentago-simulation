import numpy as np
import pygame
import sys

# Define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_SIZE = 3  # Size of each subgrid
NUM_WIN = 5  # number of pieces you need in a row to win

# Define the Pentago game class
class PentagoGame:
    def __init__(self):
        # Initialize the game board as a 2D Numpy array
        self.board = np.zeros((6, 6), dtype=int)
        self.current_player = 1  # 1 for player 1, -1 for player 2
        self.current_move = None  # Store the current move for left-click removal logic

    def make_move(self, player, move):
        row, col = move
        if self.board[row, col] == 0:
            self.board[row, col] = player
            self.current_move = move  # Store the current move for left-click removal logic

    def rotate_grid(self, quadrant, direction):
        # Implement the logic for rotating a 3x3 subgrid
        start_row, end_row, start_col, end_col = quadrant * GRID_SIZE, (quadrant + 1) * GRID_SIZE, 0, GRID_SIZE

        subgrid = np.copy(self.board[start_row:end_row, start_col:end_col])
        if direction == 'C':
            subgrid = np.rot90(subgrid, k=-1)
        elif direction == 'CC':
            subgrid = np.rot90(subgrid)

        self.board[start_row:end_row, start_col:end_col] = subgrid

    def check_winner(self):
        # Implement the logic for checking if there is a winner
        # Check rows, columns, and diagonals for a winner

        for i in range(6):
            if abs(sum(self.board[i, :])) == NUM_WIN:
                return self.board[i, 0]
            if abs(sum(self.board[:, i])) == NUM_WIN:
                return self.board[0, i]

        # Check diagonals
        if abs(sum([self.board[i, i] for i in range(6)])) == NUM_WIN:
            return self.board[0, 0]
        if abs(sum([self.board[i, 5 - i] for i in range(6)])) == NUM_WIN:
            return self.board[0, 5]

        return 0  # No winner

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
            elif event.button == 3:  # Right-click
                quadrant = col // GRID_SIZE
                direction = 'C' if row < GRID_SIZE else 'CC'
                pentago_game.rotate_grid(quadrant, direction)

            # Check for a winner
            winner = pentago_game.check_winner()
            if winner != 0:
                print(f"Player {winner} wins!")
                pygame.quit()
                sys.exit()

            # Switch to the next player
            pentago_game.current_player *= -1

    # Draw the current game state on the Pygame window
    screen.fill((89, 19, 4))  # Clear the screen

    # Draw the game board
    for row in range(6):
        for col in range(6):
            pygame.draw.rect(screen, BLACK, (col * (WINDOW_SIZE[0] // 6), row * (WINDOW_SIZE[1] // 6),
                                             WINDOW_SIZE[0] // 6, WINDOW_SIZE[1] // 6), 1)

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
    for row in range(6):
        for col in range(6):
            if col % GRID_SIZE == 0 and row % GRID_SIZE == 0:
                pygame.draw.line(screen, BLACK, (col * (WINDOW_SIZE[0] // 6), row * (WINDOW_SIZE[1] // 6)),
                                 ((col + GRID_SIZE) * (WINDOW_SIZE[0] // 6), (col + GRID_SIZE) * (WINDOW_SIZE[0] // 6)), 2)

    # Draw player turn indicator
    player_turn_text = f"Player {1 if pentago_game.current_player == 1 else 2}'s turn"
    font = pygame.font.Font(None, 36)
    text = font.render(player_turn_text, True, BLACK)
    screen.blit(text, (10, 10))

    # Update the Pygame display
    pygame.display.flip()
