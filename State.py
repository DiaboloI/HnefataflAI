from copy import deepcopy

class State:
    def __init__(self, board):
        self.board = board # list of strings

    def __eq__(self, other):
        return self.board == other.board

    def copy (self):
        newBoard = deepcopy(self.board)
        return State (newBoard)