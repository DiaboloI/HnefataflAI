import pygame
from Graphics import Graphics
from constant import *
from State import State
from Hnefatafl import Hnefatafl
#from Human_Agent import Human_Agent
import time


def main ():

    FPS = 60
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Hnefatafl')
    
    hnefatafl = Hnefatafl()
    graphics = Graphics(win)
    #agent = Human_Agent()
    run = True
    clock = pygame.time.Clock()
    graphics.draw(hnefatafl.state)
    pygame.display.update()

    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False

            #action = agent.get_Action(event)
            #puzzle.move(action)
            time.sleep(0.02)

        graphics.draw(hnefatafl.state)
        pygame.display.update()
        
    pygame.quit()

if __name__ == '__main__':
    main()
    
