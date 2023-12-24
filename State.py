from copy import deepcopy
import torch
import numpy as np

class State:
    def __init__(self, board= None, player = 1, legal_actions = []) -> None:
        self.board = board
        self.player = player
        self.legal_actions = legal_actions 

    def get_opponent (self):
        return -self.player
                    
    def switch_player(self):
        self.player = self.get_opponent()

    def score (self):
        return self.board.sum()

    def __eq__(self, other) ->bool:
        return np.equal(self.board, other.board).all() 
        # return self.board == other.board

    def __hash__(self) -> int:
        return hash(repr(self.board))
    
    def copy (self):
        newBoard = np.copy(self.board)
        # newBoard = deepcopy(self.board)
        legal_actions = self.legal_actions.copy()
        return State(board=newBoard, player=self.player, legal_actions=legal_actions)
    
    def reverse (self):
        reversed = self.copy()
        reversed.board = reversed.board * -1
        reversed.player = reversed.player * -1
        return reversed

    def toTensor (self, device = torch.device('cpu')) -> tuple:
        #print(self.board)
        board_np = self.board.reshape(-1)
        
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        actions_np = np.array(list(self.legal_actions), np.int32)
        #print(len(list(self.legal_actions)))
        #print(list(self.legal_actions)[0])
        #print(actions_np[0])
        actions_tensor = torch.from_numpy(actions_np.astype(np.int32))
        return board_tensor, actions_tensor
    
    [staticmethod]
    def tensorToState (state_tuple, player):
        board_tensor = state_tuple[0]
        board = board_tensor.reshape([11,11]).cpu().numpy()
        legal_actions_tensor = state_tuple[1]
        legal_actions = legal_actions_tensor.cpu().numpy()
        legal_actions = list(map(tuple, legal_actions))
        return State(board, player=player, legal_actions=legal_actions)
