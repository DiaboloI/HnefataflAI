import pygame
from Player import Player
from State import State
from Hnefatafl import Hnefatafl
import random

class Random_Agent:
    def __init__(self, player : Player):
        self.player = player
        self.hnefatafl = Hnefatafl()

    def getAction(self, event, graphics, state : State, attackerTurn : bool):
        actions = self.hnefatafl.getActions(attackerTurn, state)

        randomMove = random.randint(0, len(actions) - 1)
        return list(actions)[randomMove]

