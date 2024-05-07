import torch
import random
import math
from DQN_Deep import DQN
from Constant import *
from State import State

class DQN_Agent:
    def __init__(self, player = 1, parametes_path = None, train = True, env= None):
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.player = player
        self.train = train
        self.setTrainMode()

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_Action (self, state:State, epoch = 0, events= None, train = True, graphics = None, attackerTurn = 0) -> tuple:
        actions = state.legal_actions
        if self.train and train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                return random.choice(list(actions))


        state_tensor, action_tensor = state.toTensor()

        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(action_tensor),1))

        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor) # here
        max_index = torch.argmax(Q_values)
        return list(actions)[max_index]

    def get_Actions (self, states_tensor: State, dones) -> torch.tensor:
        actions = []
        boards_tensor = states_tensor[0]
        actions_tensor = states_tensor[1]
        for i, board in enumerate(boards_tensor):
            if dones[i].item():
                actions.append((0,0,0,0))
            else:
                state = State.tensorToState((boards_tensor[i],actions_tensor[i]), self.player)
                actions.append(self.get_Action(state = state, train=False))
        return torch.tensor(actions)

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        if epoch < decay:
            return start - (start - final) * epoch/decay
        return final

    def loadModel (self, file):
        self.model = torch.load(file)

    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None):
        return self.get_Action(state)
