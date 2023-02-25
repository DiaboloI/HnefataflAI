import pygame
from Player import Player
from Graphics import *

class Human_Agent:
   
    def __init__(self, player : Player) -> None:
        self.player = player

    def get_Action (self, event, graphics : Graphics):
        if event.type == pygame.MOUSEBUTTONUP:
            return graphics.calcRowcol(event.pos)
        return None
