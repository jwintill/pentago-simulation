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
        self.num_actions = 0 # 0 for no action done, 1 for one action done, 2 for two actions done, ending the turn

    def make_move(self, player, move):
        row, col = move
        if(move == self.current_move):
            self.board[row, col] = 0
            self.num_actions -= 1
            self.current_move = None
        elif self.board[row, col] == 0 and self.num_actions != 1:
            self.board[row, col] = player
            self.current_move = move  # Store the current move for left-click removal logic
            self.num_actions += 1

    def rotate_grid(self, quadrant, direction):
        # Calculate start and end indices based on quadrant
        start_row, end_row = (quadrant // 2) * GRID_SIZE, ((quadrant // 2) + 1) * GRID_SIZE
        start_col, end_col = (quadrant % 2) * GRID_SIZE, ((quadrant % 2) + 1) * GRID_SIZE

        if quadrant == 2:
            start_col, end_col = 3 - end_col, 3 - start_col

        subgrid = np.copy(self.board[start_row:end_row, start_col:end_col])
        if direction == 'CC':
            subgrid = np.rot90(subgrid, k=-1)
        elif direction == 'C':
            subgrid = np.rot90(subgrid)

        self.board[start_row:end_row, start_col:end_col] = subgrid
        self.num_actions += 1

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
            
        elif event.type == pygame.KEYDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // (WINDOW_SIZE[1] // 6)
            col = mouse_pos[0] // (WINDOW_SIZE[0] // 6)
            if event.key == pygame.K_r:  # Press 'r' key to rotate right
                quadrant = (row // 3) * 2 + (col // 3)
                direction = 'CC'
                print(quadrant)
                pentago_game.rotate_grid(quadrant, direction)

            elif event.key == pygame.K_l:  # Press 'l' key to rotate left
                quadrant = (row // 3) * 2 + (col // 3)
                direction = 'C'
                print(quadrant)
                pentago_game.rotate_grid(quadrant, direction)


            # Check for a winner
            winner = pentago_game.check_winner()
            if winner != 0:
                print(f"Player {winner} wins!")
                pygame.quit()
                sys.exit()

            # Switch to the next player
            if(pentago_game.num_actions == 2):
                pentago_game.current_player *= -1
                pentago_game.num_actions = 0

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
    pygame.draw.line(screen, WHITE, (0, WINDOW_SIZE[1] // 2),
                     (WINDOW_SIZE[0], (WINDOW_SIZE[1] // 2)), (WINDOW_SIZE[0] // 20))
    pygame.draw.line(screen, WHITE, (WINDOW_SIZE[0] // 2, 0),
                     (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]), (WINDOW_SIZE[0] // 20))


    # Draw player turn indicator
    player_turn_text = f"Player {1 if pentago_game.current_player == 1 else 2}'s turn"
    font = pygame.font.Font(None, 36)
    text = font.render(player_turn_text, True, BLACK)
    screen.blit(text, (10, 10))

    # Update the Pygame display
    pygame.display.flip()
