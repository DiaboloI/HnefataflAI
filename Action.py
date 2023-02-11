from enum import Enum

class Direction (Enum):
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

class PieceType (Enum):
    KING = 1
    ATTACKER = 2
    DEFENDER = 3

class Piece():
    row_col : tuple
    pieceType : PieceType

class Action():
    direction : Direction
    steps : int
    piece : Piece


