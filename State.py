# import numpy as np
# import torch
#
# class State:
#     def __init__(self, board= None, player = 1, legal_actions = []) -> None:
#         self.board = board
#         self.player = player
#         self.legal_actions = legal_actions
#
#     def get_opponent (self):
#         return -self.player
#
#     def switch_player(self):
#         self.player = self.get_opponent()
#
#     def __eq__(self, other) ->bool:
#         return np.equal(self.board, other.board).all()
#
#     def __hash__(self) -> int:
#         return hash(repr(self.board))
#
#     def copy (self):
#         newBoard = np.copy(self.board)
#         legal_actions = self.legal_actions.copy()
#         return State(board=newBoard, player=self.player, legal_actions=legal_actions)
#
#
#     def toTensor (self, device = torch.device('cpu')) -> tuple:
#         board_np = self.board.reshape(-1)
#         board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
#         actions_np = np.array(self.legal_actions)
#         actions_tensor = torch.from_numpy(actions_np)
#         return board_tensor, actions_tensor
#
#     [staticmethod]
#     def tensorToState (state_tuple, player):
#         board_tensor = state_tuple[0]
#         board = board_tensor.reshape([11,11]).cpu().numpy()
#         legal_actions_tensor = state_tuple[1]
#         legal_actions = legal_actions_tensor.cpu().numpy()
#         legal_actions = list(map(tuple, legal_actions))
#         return State(board, player=player, legal_actions=legal_actions)
#

from copy import deepcopy
import torch
import numpy as np

class State:
    def __init__(self, board= [], player = 1, legal_actions = []) -> None:
        self.board = board
        if (len(board) == 0):
            self.board = np.array([[0,0,0,1,1,1,1,1,0,0,0],
                          [0,0,0,0,0,1,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0],
                          [1,0,0,0,0,2,0,0,0,0,1],
                          [1,0,0,0,2,2,2,0,0,0,1],
                          [1,1,0,2,2,3,2,2,0,1,1],
                          [1,0,0,0,2,2,2,0,0,0,1],
                          [1,0,0,0,0,2,0,0,0,0,1],
                          [0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,1,0,0,0,0,0],
                          [0,0,0,1,1,1,1,1,0,0,0]])
        self.player = player
        self.legal_actions = legal_actions

        self.currentPiece = ()
        self.possibleMoves = []

        self.repetitionCount = 0
        self.repetitionPattern = []
        self.currentPattern = []

        self.moveCount = 0

        self.isDraw = False

        self.kingPos = (5, 5)

        self.extraTreat = 0

        self.whiteCaptures = 0
        self.blackCaptures = 0


    def get_opponent (self):
        return -self.player

    def switch_player(self):
        self.player = self.get_opponent()

    def __eq__(self, other) ->bool:
        return np.equal(self.board, other.board).all()
        # return self.board == other.board

    def __hash__(self) -> int:
        return hash(repr(self.board))

    def copy (self):
        newBoard = np.copy(self.board)
        # newBoard = deepcopy(self.board)
        legal_actions = self.legal_actions.copy()

        state = State(board=newBoard, player=self.player, legal_actions=legal_actions)

        state.currentPiece = self.currentPiece
        state.possibleMoves = self.possibleMoves.copy()

        state.repetitionCount = self.repetitionCount
        state.repetitionPattern = self.repetitionPattern.copy()
        state.currentPattern = self.currentPattern.copy()

        state.moveCount = self.moveCount

        state.isDraw = self.isDraw

        state.kingPos = self.kingPos

        state.extraTreat = self.extraTreat

        state.whiteCaptures = self.whiteCaptures
        state.blackCaptures = self.blackCaptures

        return state

    def toTensor (self, device = torch.device('cpu')) -> tuple:
        #print(self.board)
        board_np = self.board.reshape(-1)

        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        actions_np = np.array(list(self.legal_actions))
        #print(len(list(self.legal_actions)))
        #print(list(self.legal_actions)[0])
        #print(actions_np[0])
        actions_tensor = torch.tensor(actions_np,dtype=torch.float32)
        return board_tensor, actions_tensor

    [staticmethod]
    def tensorToState (state_tuple, player):
        board_tensor = state_tuple[0]
        board = board_tensor.reshape([11,11]).cpu().numpy()
        legal_actions_tensor = state_tuple[1]
        legal_actions = legal_actions_tensor.cpu().numpy()
        legal_actions = list(map(tuple, legal_actions))
        #print(legal_actions)
        return State(board, player=player, legal_actions=legal_actions)


