import pygame
from Graphics import Graphics
from Human_Agent import Human_Agent
from Ai_Agent import Ai_Agent
from Random_Agent import Random_Agent
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
    #attacker = Ai_Agent(Player.ATTACKER)
    #defender = Human_Agent(Player.DEFENDER)
    defender = Ai_Agent(Player.DEFENDER)
    #defender = Random_Agent(Player.DEFENDER)
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
            action = player.getAction(event, graphics, hnefatafl.state, player == attacker)
        if action:
            if type(player) is Human_Agent:
                possibleMoves, moved = hnefatafl.handleMouseClick(action, player == attacker)
            else:
                hnefatafl.state = hnefatafl.move(action[0], action[1], hnefatafl.state)
                moved = True
            

            if moved: # change turn.
                if player == attacker:
                    player = defender
                else:
                    player = attacker
                won = hnefatafl.isWon(hnefatafl.state)
            action = None

        
        graphics.draw(hnefatafl.state, possibleMoves, player == attacker)
        pygame.display.update()
        
        if won:
            run = False
            if won is str: # draw
                print ("The game ends in a draw: " + str(won) + ".")
            else:
                graphics.drawWinningMessage(won)
                pygame.display.update()
                print (str(won) + " won!")
                time.sleep(20)
        

       
    pygame.quit()
    

def printBoard(state : State): # for debugging
    for row in state.board:
        print(row)

if __name__ == '__main__':
    main()
    
