import pygame

class Game():
    def __init__(self, id):
        self.id = id
        self.GRID_SIZE = 8
        self.CELL_SIZE = 80
        self.BLACK_MOVES = {"Pawn":[(1, 0)]}
        self.WHITE_MOVES = {"Pawn":[(-1, 0)]}
        self.MOVES = {
                "Knight":[(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)],
                "Rook":(4, 8),
                "Bishop": (4, 8),
                "Queen": (8, 8),
                "King": [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                }