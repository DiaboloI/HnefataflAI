import pygame
from Graphics import Graphics
from Human_Agent import Human_Agent
from Player import Player
from constant import *
from State import State
from Hnefatafl import Hnefatafl
import time


def main ():

    FPS = 60
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Hnefatafl')
    
    hnefatafl = Hnefatafl()
    graphics = Graphics(win)
    attacker = Human_Agent(Player.ATTACKER)
    defender = Human_Agent(Player.DEFENDER)
    run = True
    clock = pygame.time.Clock()
    graphics.draw(hnefatafl.state, [], True)
    pygame.display.update()
    
    player = attacker
    possibleMoves = []
    moved = False
    
    action = None
    won = None

    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False
            action = player.get_Action(event, graphics)
        if action:
            possibleMoves, moved = hnefatafl.handleMouseClick(action, player == attacker)
            if moved:
                if player == attacker:
                    player = defender
                else:
                    player = attacker
                won = hnefatafl.isWon()
            action = None


        graphics.draw(hnefatafl.state, possibleMoves, player == attacker)
        pygame.display.update()
        
        if won:
            run = False
            print (str(won) + " won!") #TODO: make a caption on the screen announcing the victory.
        

       
    pygame.quit()
    

if __name__ == '__main__':
    main()
    
