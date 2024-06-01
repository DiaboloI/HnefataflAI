from Random_Agent import Random_Agent
from DQN_Agent_Deep import DQN_Agent
from Hnefatafl import Hnefatafl
from Player import Player
import pygame
from Graphics import Graphics
from Human_Agent import Human_Agent
from Ai_Agent import Ai_Agent
from Player import Player
from Constant import *
from State import State
import time

class Tester:
    def __init__(self, env, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2
        

    def test2(self, games_num):
        FPS = 60
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Hnefatafl')

        graphics = Graphics(win)

        env = self.env
        player = self.player1
        player1_win = 0
        player2_win = 0
        draw_count = 0
        games = 0
        run = True
        clock = pygame.time.Clock()
        graphics.draw(env.state, [], True)
        pygame.display.update()

        while(run):
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
            while games < games_num:
                #print(str(env.state.board))
                time.sleep(0.5)
                action = player.get_Action(state=env.state)
                env.move(action, env.state)
                player = self.switchPlayers(player)
                endGame = env.is_end_of_game(env.state)

                graphics.draw(env.state, [], player.player == 1)
                pygame.display.update()

                if endGame:
                    graphics.drawWinningMessage(endGame)
                    pygame.display.update()
                    print (str(endGame) + " won!")
                    time.sleep(2)

                    if endGame == Player.ATTACKER:
                        player1_win += 1
                    elif endGame == Player.DEFENDER:
                        player2_win += 1
                    elif endGame == "draw":
                        draw_count += 1
                    env.state = env.get_init_state()
                    games += 1
                    player = self.player1

        pygame.quit()
        return player1_win, player2_win, draw_count




    def test (self, games_num):
        env = self.env
        env.sWcaptures = 0
        env.sBcaptures = 0
        player = self.player1
        player1_win = 0
        player2_win = 0
        draws = 0
        games = 0
        while games < games_num:

            action = player.get_Action(state=env.state, train = False)
            #print("In test: ", action)
            env.move(action, env.state)
            player = self.switchPlayers(player)
            endGame = env.is_end_of_game(env.state)
            if endGame:
                print(games, end='\r')
                if endGame == Player.ATTACKER:
                    player1_win += 1
                elif endGame == Player.DEFENDER:
                    player2_win += 1
                elif endGame == "draw":
                    draws += 1

                env.state = env.get_init_state()

                games += 1
                player = self.player1
        print("w: ", env.sWcaptures, " b: ", env.sBcaptures)
        env.sWcaptures = 0
        env.sBcaptures = 0
        return player1_win, player2_win, draws



    # def test (self, games_num):
    #     env = self.env
    #     player = self.player1
    #     player1_win = 0
    #     player2_win = 0
    #     draw_count = 0
    #     games = 0
    #     while games < games_num:
    #         #print(str(env.state.board))
    #         action = player.get_Action(state=env.state)
    #         env.move(action, env.state)
    #         player = self.switchPlayers(player)
    #         endGame = env.is_end_of_game(env.state)
    #         if endGame:
    #             if endGame == Player.ATTACKER:
    #                 player1_win += 1
    #             elif endGame == Player.DEFENDER:
    #                 player2_win += 1
    #             elif endGame == "draw":
    #                 draw_count += 1
    #             env.state = env.get_init_state()
    #             games += 1
    #             player = self.player1
    #     return player1_win, player2_win, draw_count

    def switchPlayers(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def __call__(self, games_num):
        return self.test(games_num)

agents = [71, 90, 91, 92, 93, 101, 111]
agentsAttackers = [91, 93, 101]
agents2 = [20, 40, 50, 60, 70, 80]
agents2Attackers = [60, 50, 40]
if __name__ == '__main__':
    env = Hnefatafl()

    # print("AI Defender:")
    # player1 = Random_Agent(env=env, player=1)
    # player2 = Ai_Agent(Player.DEFENDER)
    # test = Tester(env,player1, player2)
    # print(test.test(100), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    # env.sWcaptures = 0
    # env.sBcaptures = 0
    #
    # print("AI Attacker:")
    # player1 = Ai_Agent(Player.ATTACKER)
    # player2 = Random_Agent(env=env, player=-1)
    # test = Tester(env,player1, player2)
    # print(test.test(100), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    # env.sWcaptures = 0
    # env.sBcaptures = 0
    #
    # for agent in []:
    #     bp = f"Data/best_params_{agent}.pth"
    #     brp = f"Data/best_random_params_{agent}.pth"
    #
    #     print(f"agent {agent}:")
    #     print("------------------")
    #     print("against Random agent:")
    #     print(f"best_paramas:")
    #     print("attacker:")
    #     player1 = DQN_Agent(env=env, player=1, train=False, parametes_path=bp)
    #     player2 = Random_Agent(env=env, player=-1)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(100), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #
    #     print("defender:")
    #     player1 = Random_Agent(env=env, player=1)
    #     player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path=bp)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(100), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #
    #     print(f"best_random:")
    #     print("attacker:")
    #     player1 = DQN_Agent(env=env, player=1, train=False, parametes_path=brp)
    #     player2 = Random_Agent(env=env, player=-1)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(100), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #
    #     print("defender:")
    #     player1 = Random_Agent(env=env, player=1)
    #     player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path=brp)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(100), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #     #
    #     print("------------------")
    #     print("against AI agent:")
    #     print(f"best_paramas:")
    #     print("attacker:")
    #     player1 = DQN_Agent(env=env, player=1, train=False, parametes_path=bp)
    #     player2 = Ai_Agent(Player.DEFENDER)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(1), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #
    #     print("defender:")
    #     player1 = Ai_Agent(Player.ATTACKER)
    #     player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path=bp)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(1), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #
    #     print(f"best_random:")
    #     print("attacker:")
    #     player1 = DQN_Agent(env=env, player=1, train=False, parametes_path=brp)
    #     player2 = Ai_Agent(Player.DEFENDER)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(1), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #
    #     print("defender:")
    #     player1 = Ai_Agent(Player.ATTACKER)
    #     player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path=brp)
    #     test = Tester(env,player1, player2)
    #
    #     print(test.test(1), "; w: ", env.sWcaptures, " b: ", env.sBcaptures)
    #     env.sWcaptures = 0
    #     env.sBcaptures = 0
    #
    #     print("-----------------------------------------")


    # player1 = Random_Agent(env=env, player=1)
    # player2 = Random_Agent(env=env, player=-1)
    # test = Tester(env,player1, player2)
    # print("Random VS Random:")
    # print(test.test(1000))



#     #player1 = Random_Agent(env=env, player=1)
#     player1 = DQN_Agent(env=env, player=1, train=False, parametes_path="Data/best_params_101.pth") # TODO: Wrong
#     #player2 = Random_Agent(env=env, player=-1)
#     player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path="Data/best_params_111.pth") # TODO: Wrong
#     test = Tester(env,player1, player2)
#     print("Black VS White")
#     #print(test.test(1000))
#
#     player1 = Random_Agent(env=env, player=1)
#     #player2 = Random_Agent(env=env, player=-1)
#     player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path="Data/best_params_111.pth") # TODO: Wrong
#     test = Tester(env,player1, player2)
#     print("Black best_paramas VS Random")
#     print(test.test(1000))
#
#     print (env.sWcaptures, " b: ", env.sBcaptures)
#     env.sWcaptures = 0
#     env.sBcaptures = 0
#
#     player1 = Random_Agent(env=env, player=1)
#     player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path="Data/best_random_params_111.pth") # TODO: Wrong
#     test = Tester(env,player1, player2)
#     print("Black best_random VS Random")
#     print(test.test(1000))
#
#     print (env.sWcaptures, " b: ", env.sBcaptures)
#     env.sWcaptures = 0
#     env.sBcaptures = 0
#
    player1 = DQN_Agent(env=env, player=1, train=False, parametes_path="Data/best_params_95.pth") # TODO: Wrong
    #player1 = Random_Agent(env=env, player=1)
    player2 = Random_Agent(env=env, player=-1)
    test = Tester(env,player1, player2)
    print("White best_params VS Random")
    print(test.test(1000))

    print (env.sWcaptures, " b: ", env.sBcaptures)
    env.sWcaptures = 0
    env.sBcaptures = 0

    player1 = DQN_Agent(env=env, player=1, train=False, parametes_path="Data/best_random_params_95.pth") # TODO: Wrong
    #player1 = Random_Agent(env=env, player=1)
    player2 = Random_Agent(env=env, player=-1)
    test = Tester(env,player1, player2)
    print("White best_random VS Random")
    print(test.test(1000))

    print (env.sWcaptures, " b: ", env.sBcaptures)



