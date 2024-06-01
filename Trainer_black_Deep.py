from Hnefatafl import Hnefatafl

from DQN_Agent_Deep import DQN_Agent
from ReplayBuffer import ReplayBuffer
from Random_Agent import Random_Agent
from Fix_Agent import Fix_Agent
import torch
from Tester import Tester
import requests

epochs = 2000000
start_epoch = 184000
C = 4
learning_rate = 0.001
batch_size = 64
env = Hnefatafl()
MIN_Buffer = 4000

File_Num = 75
path_load= f'Data/best_params_71.pth'
path_Save=f'Data/params_{File_Num}.pth'
path_best = f'Data/best_params_{File_Num}.pth'
buffer_path = f'Data/buffer_{File_Num}.pth'
results_path=f'Data/results_{File_Num}.pth'
random_results_path = f'Data/random_results_{File_Num}.pth'
path_best_random = f'Data/best_random_params_{File_Num}.pth'


def main ():
    
    player1 = DQN_Agent(player=-1, env=env,parametes_path=path_Save)
    player_hat = DQN_Agent(player=-1, env=env, train=False)
    Q = player1.DQN
    Q_hat = Q.copy()
    Q_hat.train = False
    player_hat.DQN = Q_hat
    
    #player2 = Fix_Agent(player=1, env=env, train=True, random=0) # 0.1
    player2 = Random_Agent(player=1, env=env)
    buffer = ReplayBuffer(path='')

    results_file = torch.load(results_path)
    results = results_file['results']
    avgLosses = results_file['avglosses']     #[]
    avgLoss = avgLosses[-1] #0
    loss = torch.Tensor([0])
    res = 0
    best_res = 200
    loss_count = 0
    tester = Tester(player1=Random_Agent(player=1, env=env), player2=player1, env=env)
    #tester_fix = Tester(player1=player2, player2=player1, env=env)
    random_results = []
    best_random = 0
    

    # init optimizer
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optim,100000*30, gamma=0.90)
    #scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[30*50000, 30*100000, 30*250000, 30*500000], gamma=0.5)
    
    for epoch in range(start_epoch, epochs):
        print(f'epoch = {epoch}', end='\r')
        state = env.get_init_state()
        action = player2.get_Action(state=state)
        state_1_R = env.get_next_state(state=state, action=action)
        #print(state_1.board)
        #state_1_R = state_1.reverse()
        end_of_game_2 = False
        while not end_of_game_2:
            #print("just " + str(epoch))
            # Sample Environement
            action_1_R = player1.get_Action(state_1_R, epoch=epoch) # fix add param
            after_state_1_R = env.get_next_state(state=state_1_R, action=action_1_R)
            reward_1_R, end_of_game_1_R = env.reward(after_state_1_R)
            if end_of_game_1_R:
                res += reward_1_R
                #print("reward " + str(epoch))
                buffer.push(state_1_R, action_1_R, -reward_1_R, after_state_1_R, True)
                break
            state_2 = after_state_1_R
            action_2 = player2.get_Action(state=state_2)
            after_state_2 = env.get_next_state(state=state_2, action=action_2)
            reward_2_R, end_of_game_2 = env.reward(state=after_state_2)
            if end_of_game_2:
                res += reward_2_R
                #print(after_state_2.board)
                #print("reward two " + str(epoch))
            buffer.push(state_1_R, action_1_R, -reward_2_R, after_state_2, end_of_game_2)
            #print(len(buffer))
            state_1_R = after_state_2

            if len(buffer) < MIN_Buffer:
                continue
            
            # Train NN
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = Q(states[0], actions)
            next_actions = player1.get_Actions(next_states, dones)
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states[0], next_actions)

            loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            
            scheduler.step()
            if loss_count <= 1000:
                avgLoss = (avgLoss * loss_count + loss.item()) / (loss_count + 1)
                loss_count += 1
            else:
                avgLoss += (loss.item()-avgLoss)* 0.00001 
        

        if epoch % C == 0:
                Q_hat.load_state_dict(Q.state_dict())

        if (epoch+1) % 100 == 0:
            print(f'\nres= {res}')
            avgLosses.append(avgLoss)
            results.append(res)
            if best_res > res:
                best_res = res
                player1.save_param(path_best)
            res = 0

        if (epoch+1) % 1000 == 0:
            test = tester(100)
            test_score = test[1]
            if best_random < test_score:
                best_random = test_score
                player1.save_param(path_best_random)
            print(test)
            try: 
                r = requests.post("https://ntfy.sh/dqnhnefatafltraining2", data=f'In epoch {epoch+1}, test results: {test}, averageloss: {avgLoss}, best_random: {best_random},, best res: {best_res}'.encode(encoding='utf-8'))
                r.raise_for_status() 
            except requests.exceptions.RequestException as errex: 
                print("Exception request") 
            random_results.append(test_score)

        if (epoch+1) % 1000 == 0:
            torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
            player1.save_param(path_Save)
            torch.save(random_results, random_results_path)

        if (epoch+1) % 5000 == 0:
            torch.save(buffer, buffer_path)

        if len(buffer) > MIN_Buffer:
            print (f'epoch={epoch} loss={loss:.5f} Q_values[0]={Q_values[0].item():.3f} avgloss={avgLoss:.5f}', end=" ")
            print (f'learning rate={scheduler.get_last_lr()[0]} path={path_Save} res= {res} best_res = {best_res}')

    torch.save({'epoch': epoch, 'results': results, 'avglosses':avgLosses}, results_path)
    torch.save(buffer, buffer_path)
    torch.save(random_results, random_results_path)

if __name__ == '__main__':
    main()


