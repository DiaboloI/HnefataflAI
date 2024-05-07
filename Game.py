import pygame
from Graphics import Graphics
from Human_Agent import Human_Agent
from Ai_Agent import Ai_Agent
from Random_Agent import Random_Agent
from DQN_Agent_Deep import DQN_Agent
from Player import Player
from Constant import *
from State import State
from Hnefatafl import Hnefatafl
import time

File_Num = 20
path_Save=f'Data/best_params_{File_Num}.pth'

def main ():

    FPS = 60
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Hnefatafl')
    
    hnefatafl = Hnefatafl()
    graphics = Graphics(win)
    graphics.onGame = True
    attacker = Human_Agent(Player.ATTACKER)
    #attacker = Random_Agent(Player.ATTACKER, hnefatafl)
    #attacker = DQN_Agent(Player.ATTACKER, path_Save, False, hnefatafl)
    #attacker = Ai_Agent(Player.ATTACKER)
    defender = Human_Agent(Player.DEFENDER)
    #defender = Ai_Agent(Player.DEFENDER)
    #defender = Random_Agent(Player.DEFENDER, hnefatafl)
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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
               run = False

        action = player.get_Action(state=hnefatafl.state, events=events, graphics=graphics, attackerTurn=(player == attacker))
        if action:
            if type(player) is Human_Agent:
                possibleMoves, moved = hnefatafl.handleMouseClick(action, player == attacker)
            else:
                hnefatafl.move(action, hnefatafl.state)
                moved = True
            
            time.sleep(0.5)
            if moved: # change turn.
                graphics.moveCount += 1
                if player == attacker:
                    player = defender
                else:
                    player = attacker
                won = hnefatafl.is_end_of_game(hnefatafl.state)
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
    
