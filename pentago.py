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
        self.hasPlaced = False
        self.hasRotated = False

    def make_move(self, player, move):
        row, col = move
        if(move == self.current_move):
            self.board[row, col] = 0
            self.hasPlaced = False
            self.current_move = None
        elif self.board[row, col] == 0 and not self.hasPlaced:
            self.board[row, col] = player
            self.current_move = move  # Store the current move for left-click removal logic
            self.hasPlaced = True

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
        self.hasRotated = True

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
