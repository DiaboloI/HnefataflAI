import pygame
from Player import Player
from State import State
from Hnefatafl import Hnefatafl
import random

class Random_Agent:
    def __init__(self, player : Player, env):
        self.player = player
        self.hnefatafl = Hnefatafl()

    def get_Action(self, events = None, graphics = None, state : State = None, train = False):
        actions = self.hnefatafl.getActions(self.player == 1, state)
        if (len(actions) == 1):
            return list(actions)[0]
        randomMove = random.randint(0, len(actions) - 1)
        return list(actions)[randomMove]

