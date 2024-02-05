from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent
from Hnefatafl import Hnefatafl
from Player import Player

class Tester:
    def __init__(self, env, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2
        

    def test (self, games_num):
        env = self.env
        player = self.player1
        player1_win = 0
        player2_win = 0
        draws = 0
        games = 0
        while games < games_num:
            action = player.get_Action(state=env.state)
            env.move(action, env.state)
            player = self.switchPlayers(player)
            iswin = env.is_end_of_game(env.state)
            if (iswin != None):
                if iswin == Player.ATTACKER:
                    player1_win += 1
                elif iswin == Player.DEFENDER:
                    player2_win += 1
                elif iswin == "repetition":
                    draws += 1
                env.state = env.get_init_state()
                games += 1
                player = self.player1
        return player1_win, player2_win, draws        

    def switchPlayers(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def __call__(self, games_num):
        return self.test(games_num)

if __name__ == '__main__':
    env = Hnefatafl()
    player1 = Random_Agent(env=env, player=1)
    player2 = Random_Agent(env=env, player=-1)
    #player2 = DQN_Agent(env=env, player=-1, train=False, parametes_path="Data/params_15.pth") # TODO: Wrong
    test = Tester(env,player1, player2)
    print(test.test(100))
    player1 = DQN_Agent(env=env, player=1, train=False, parametes_path="Data/params_15.pth") # TODO: Wrong
    #player1 = Random_Agent(env=env, player=1)
    player2 = Random_Agent(env=env, player=-1)
    test = Tester(env,player1, player2)
    print(test.test(100))
