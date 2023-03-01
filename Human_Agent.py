import pygame
from Player import Player
from Graphics import *

class Human_Agent:
   
    def __init__(self, player : Player) -> None:
        self.player = player

    def getAction (self, event, graphics : Graphics, state, attackerTurn : bool):
        if event.type == pygame.MOUSEBUTTONUP:
            return graphics.calcRowcol(event.pos)
        return None