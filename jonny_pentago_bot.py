class JonnyBot:
    def __init__(self, color, board):
        self.color = color
        self.board = board

    def update_board(self, board):
        self.board = board

    def compute_move(self):
        move = (0,0)
        return move
    
    def compute_rotation(self):
        quadrant = 0
        direction = 'C'
        return quadrant, direction
