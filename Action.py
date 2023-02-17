from enum import Enum

class Direction (Enum):
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

class Action():
    direction : Direction
    steps : int
    pos : tuple


