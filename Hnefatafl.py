# Environment
from typing import AsyncContextManager
from constant import *
from State import State
from Action import Action

class Hnefatafl:

    def __init__(self, state:State = None):
        if state == None:
            self.state = self.getStartingPosition()
        else:
            self.state = state

    def getStartingPosition(self):
        board = ["...aaaaa...",
                 ".....a.....",
                 "...........",
                 "a....d....a",
                 "a...ddd...a",
                 "aa.ddkdd.aa",
                 "a...ddd...a",
                 "a....d....a",
                 "...........",
                 ".....a.....",
                 "...aaaaa..."]

        return State(board)

    def is_legal_action (self, action: Action, state:State = None):
        pass
        

    def get_actions (self, state: State = None):
        pass

    def move (self, action: Action):
        pass
