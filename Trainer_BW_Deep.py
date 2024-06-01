from Hnefatafl import Hnefatafl

from DQN_Agent_Deep import DQN_Agent
from ReplayBuffer import ReplayBuffer
from Random_Agent import Random_Agent
import torch
from Tester import Tester

import requests

epochs = 3000000
start_epoch = 595000
C = 4
learning_rate = 0.0001
batch_size = 64
env = Hnefatafl()
MIN_Buffer = 4000

File_Num_white = 101
path_load_white= f'Data/best_random_params_91.pth'
path_Save_white=f'Data/params_{File_Num_white}.pth'
path_best_white = f'Data/best_params_{File_Num_white}.pth'
buffer_path_white = f'Data/buffer_{File_Num_white}.pth'
results_path_white=f'Data/results_{File_Num_white}.pth'
random_results_path_white = f'Data/random_results_{File_Num_white}.pth'
path_best_random_white = f'Data/best_random_params_{File_Num_white}.pth'

File_Num_black = 111
path_load_black= f'Data/best_params_71.pth'
path_Save_black=f'Data/params_{File_Num_black}.pth'
path_best_black = f'Data/best_params_{File_Num_black}.pth'
buffer_path_black = f'Data/buffer_{File_Num_black}.pth'
results_path_black=f'Data/results_{File_Num_black}.pth'
random_results_path_black = f'Data/random_results_{File_Num_black}.pth'
path_best_random_black = f'Data/best_random_params_{File_Num_black}.pth'

# Since Hnefatafl is an assymetric game, in the black-white trainer two seperate agents need to be trained and not only
# one, as would be done with a symmetric game like Chess or Checkers. Therefore, the training will not be faster, but
# would be against a more sophisticated agent than the simple Random Agent.


def main ():

    # attacker:
    player1 = DQN_Agent(player=1, env=env,parametes_path=path_Save_white)
    player_hat1 = DQN_Agent(player=1, env=env,train=False)

    Q1 = player1.DQN
    Q1_hat = Q1.copy()
    Q1_hat.train = False
    player_hat1.DQN = Q1_hat

    # defender:
    player2 = DQN_Agent(player=-1, env=env,parametes_path=path_Save_black)
    player_hat2 = DQN_Agent(player=-1, env=env,train=False)

    Q2 = player2.DQN
    Q2_hat = Q2.copy()
    Q2_hat.train = False
    player_hat2.DQN = Q2_hat




    buffer1 = ReplayBuffer(path='') # None

    buffer2 = ReplayBuffer(path='') # None

    results_file1 = None # torch.load(results_path)
    results1 =  [] #results_file['results'] # []
    avgLosses1 = []  #results_file['avglosses']     #[]
    avgLoss1 = 0 #avgLosses[-1] # 0
    loss1 = torch.Tensor([0])
    res1 = 0
    best_res1 = -200
    loss_count1 = 0

    results_file2 = None # torch.load(results_path)
    results2 =  [] #results_file['results'] # []
    avgLosses2 = []  #results_file['avglosses']     #[]
    avgLoss2 = 0 #avgLosses[-1] # 0
    loss2 = torch.Tensor([0])
    res2 = 0
    best_res2 = 200
    loss_count2 = 0

    tester_random1 = Tester(player1=player1, player2=Random_Agent(player=-1, env=env), env=env)
    tester_random2 = Tester(player1=Random_Agent(player=1, env=env), player2=player2, env=env)

    random_results1 = [] #torch.load(random_results_path)   # []
    best_random1 = 0 # max(random_results)# -100

    random_results2 = [] #torch.load(random_results_path)   # []
    best_random2 = 0 # max(random_results)# -100

    # init optimizer
    optim1 = torch.optim.Adam(Q1.parameters(), lr=learning_rate)
    scheduler1 = torch.optim.lr_scheduler.StepLR(optim1,100000*30, gamma=0.90)

    # init optimizer
    optim2 = torch.optim.Adam(Q2.parameters(), lr=learning_rate)
    scheduler2 = torch.optim.lr_scheduler.StepLR(optim2,100000*30, gamma=0.90)
    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[30*50000, 30*100000, 30*250000, 30*500000], gamma=0.5)

    for epoch in range(start_epoch, epochs):
        print(f'epoch = {epoch}', end='\r')
        state_1 = env.get_init_state()
        state_2, action_2, after_state_2 = None, None, None
        end_of_game_1 = False
        end_of_game_2 = False
        while not end_of_game_1 and not end_of_game_2:
        # Sample Environement
            # white
            action_1 = player1.get_Action(state_1, epoch=epoch)
            after_state_1 = env.get_next_state(state=state_1, action=action_1)
            reward_1, end_of_game_1 = env.reward(after_state_1)
            if state_2: # not the first action in a game
                    buffer2.push(state_2, action_2, reward_1, after_state_1, end_of_game_1)    # for black #TODO: not sure
            if end_of_game_1:
                res1 += reward_1
                res2 += reward_1
                buffer1.push(state_1, action_1, -reward_1, after_state_1, True) # for white
                state_1 = after_state_1
            else:
                # Black
                state_2 = after_state_1
                action_2 = player2.get_Action(state=state_2, epoch=epoch)
                after_state_2 = env.get_next_state(state=state_2, action=action_2)
                reward_2, end_of_game_2 = env.reward(state=after_state_2)
                if end_of_game_2:
                    res2 += reward_2
                    res1 += reward_2
                    buffer2.push(state_2, action_2, -reward_2, after_state_2, True) # for black
                buffer1.push(state_1, action_1, reward_2, after_state_2, end_of_game_2)
                #buffer2.push(state_2, action_2, -reward_2, after_state_2, end_of_game_2) # for black
                state_1 = after_state_2

            if len(buffer1) < MIN_Buffer:
                continue
            if len(buffer2) < MIN_Buffer:
                continue

            # Train NN white
            states1, actions1, rewards1, next_states1, dones1 = buffer1.sample(batch_size)
            Q1_values = Q1(states1[0], actions1)
            next_actions1 = player1.get_Actions(next_states1, dones1)
            with torch.no_grad():
                Q1_hat_Values = Q1_hat(next_states1[0], next_actions1)

            loss1 = Q1.loss(Q1_values, rewards1, Q1_hat_Values, dones1)
            loss1.backward()
            optim1.step()
            optim1.zero_grad()
            scheduler1.step()

            if loss_count1 <= 1000:
                avgLoss1 = (avgLoss1 * loss_count1 + loss1.item()) / (loss_count1 + 1)
                loss_count1 += 1
            else:
                avgLoss1 += (loss1.item()-avgLoss1)* 0.00001

             # Train NN black
            states2, actions2, rewards2, next_states2, dones2 = buffer2.sample(batch_size)
            Q2_values = Q2(states2[0], actions2)
            next_actions2 = player2.get_Actions(next_states2, dones2)
            with torch.no_grad():
                Q2_hat_Values = Q2_hat(next_states2[0], next_actions2)

            loss2 = Q2.loss(Q2_values, rewards2, Q2_hat_Values, dones2)
            loss2.backward()
            optim2.step()
            optim2.zero_grad()
            scheduler2.step()

            if loss_count2 <= 1000:
                avgLoss2 = (avgLoss2 * loss_count2 + loss2.item()) / (loss_count2 + 1)
                loss_count2 += 1
            else:
                avgLoss2 += (loss2.item()-avgLoss2)* 0.00001

        if epoch % C == 0:
            Q1_hat.load_state_dict(Q1.state_dict())
            Q2_hat.load_state_dict(Q2.state_dict())

        if (epoch+1) % 100 == 0:
            print(f'\nres= {res1}')
            avgLosses1.append(avgLoss1)
            results1.append(res1)
            if best_res1 < res1:
                best_res1 = res1
                player1.save_param(path_best_white)
            res1 = 0

            print(f'\nres= {res2}')
            avgLosses2.append(avgLoss2)
            results2.append(res2)
            if best_res2 > res2:
                best_res2 = res2
                player2.save_param(path_best_black)
            res2 = 0

        if (epoch+1) % 1000 == 0:
            test1 = tester_random1(100)
            test_score1 = test1[0]

            test2 = tester_random2(100)
            test_score2 = test2[1]

            if best_random1 < test_score1:
                best_random1 = test_score1
                player1.save_param(path_best_random_white)

            if best_random2 < test_score2:
                best_random2 = test_score2
                player2.save_param(path_best_random_black)

            print('WHITE: test',test1, 'best_random:', best_random1)
            print('BLACK: test',test2, 'best_random:', best_random2)

            try:
                r = requests.post("https://ntfy.sh/dqnhnefatafltraining2", data=f'In epoch {epoch+1}: WHITE: test results: {test1}, averageloss: {avgLoss1}, best_random: {best_random1}, best_res: {best_res1}. BLACK: test results: {test2}, averageloss: {avgLoss2}, best_random: {best_random2}, best_res: {best_res2}'.encode(encoding='utf-8'))
                r.raise_for_status()
            except requests.exceptions.RequestException as errex:
                print("Exception request")

            random_results1.append(test_score1)
            random_results2.append(test_score2)

        if (epoch+1) % 5000 == 0:
            torch.save({'epoch': epoch, 'results': results1, 'avglosses':avgLosses1}, results_path_white)
            torch.save(buffer1, buffer_path_white)
            player1.save_param(path_Save_white)
            torch.save(random_results1, random_results_path_white)

            torch.save({'epoch': epoch, 'results': results2, 'avglosses':avgLosses2}, results_path_black)
            torch.save(buffer2, buffer_path_black)
            player2.save_param(path_Save_black)
            torch.save(random_results2, random_results_path_black)

        if len(buffer1) > MIN_Buffer and len(buffer2) > MIN_Buffer:
            print (f'WHITE: epoch={epoch} loss={loss1:.5f} Q_values[0]={Q1_values[0].item():.3f} avgloss={avgLoss1:.5f}', end=" ")
            print (f'WHITE: learning rate={scheduler1.get_last_lr()[0]} path={path_Save_white} res= {res1} best_res = {best_res1}')
            print (f'BLACK: epoch={epoch} loss={loss2:.5f} Q_values[0]={Q2_values[0].item():.3f} avgloss={avgLoss2:.5f}', end=" ")
            print (f'BLACK: learning rate={scheduler2.get_last_lr()[0]} path={path_Save_black} res= {res2} best_res = {best_res2}')

    torch.save({'epoch': epoch, 'results': results1, 'avglosses':avgLosses1}, results_path_white)
    torch.save(buffer1, buffer_path_white)
    torch.save(random_results1, random_results_path_white)

    torch.save({'epoch': epoch, 'results': results2, 'avglosses':avgLosses2}, results_path_black)
    torch.save(buffer2, buffer_path_black)
    torch.save(random_results2, random_results_path_black)

if __name__ == '__main__':
    main()

