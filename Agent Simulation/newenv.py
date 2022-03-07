#%% 1. Imports 
# open gym ai
from gym import Env,spaces

# helper
import numpy as np
import os
from statistics import mean
from reward import happiness
from visual import plot

# baselines
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv

#%% 2. Environment Class 
""" 
    This is simulated environment that will be integrated with Camelot
    Consists of actions,states,rewards
    Also logic for actions and NPC stats
"""

class CamelotEnv(Env):
    def __init__(self,max_training_length=10000):
        self.action_space = spaces.Discrete(8) #8 actions
        self.observation_space = spaces.Box(np.array([0,0,0,0]),np.array([100,100,100,100]))

        self.health = 100
        self.hunger = 100
        self.energy = 100
        self.wealth = 100
        self.state = (self.health, self.hunger, self.energy,self.wealth) # initial state
        self.stat_record = [[self.health],
                            [self.hunger],
                            [self.energy],
                            [self.wealth]]

        self.max_training_length = max_training_length
        self.training_length = max_training_length


    def get_action_meanings(self):
        return {0: "Eat poison apple",
                1: "Eat magic apple",
                2: "Eat force apple",
                3: "Eat heart apple",
                4: "Sleep",
                5: "Do nothing",
                6: "Sell Item",
                7: "Buy Item"
}

    def step(self, action):
        
        '''actions'''  #-------- utilize dictionaries for future complexity --------#
        if action == 0:           # "Eat poison apple"
            self.health -= 10
            self.hunger -= 5
        elif action == 1:         # "Eat magic apple"
            self.health += 10
            self.hunger += 3
        elif action == 2:         # "Eat apple"
            self.hunger += 15
        elif action == 3:         # "Eat heart apple"
            self.health += 15
            self.hunger += 2
        elif action == 4:         # "Sleep"
            self.health += 5
            self.energy += 25
        elif action == 5:
            pass
        elif action == 6:         # "Sell Item"
            self.wealth += 10
        elif action == 7:         # "Buy Item"
            self.wealth -= 10
            self.hunger += 15
        

        '''environment logic'''
        # reduce health, hunger, and energy
        self.hunger -= 5 if self.hunger > 0 else self.hunger
        self.energy -= 3 if self.energy > 0 else self.energy
        if self.hunger <= 0 or self.energy <= 0:
            self.health -= 10

        if self.hunger >= 100:
            self.hunger = 100
        if self.hunger <= 0:
            self.hunger = 0
        if self.energy >= 100:
            self.energy = 100
        if self.energy <= 0:
            self.energy = 0
        if self.health >= 100:
            self.health = 100
        if self.health <= 0:
            self.health = 0


        '''step conditions'''
        # Reduce training step by 1 per step
        self.training_length -= 1 

        ''''Record History'''
        self.state = (self.health, self.hunger, self.energy,self.wealth)
        for i in range(len(self.stat_record)):
            self.stat_record[i].append(self.state[i])
        
        # Reward per step.
        reward = 0.5 + happiness(self.state)
        
        # Check if training_length is done or if NPC health is done
        done = True if self.training_length <= 0 or self.health <= 0 else False 
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info
    
    def render(self):
        # Implement viz in camelot
        plot(self.stat_record)
        #pass

    def reset(self):
        # Reset NPC State
        self.health = 100
        self.hunger = 100
        self.energy = 100
        self.wealth = 100
        # Reset training step
        self.stat_record = [[self.health],
                            [self.hunger],
                            [self.energy],
                            [self.wealth]]
        self.training_length = self.max_training_length
        return self.state
# %% testing the environment
env = CamelotEnv(1000)
mean_score = []

episodes = 10
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        #env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{:.2f}'.format(episode, score))
    mean_score.append(score)
#env.close()

print('Total Episodes:{} Average Score:{:.2f}'.format(episode, mean(mean_score))) #get mean scores


#env.observation_space.sample()
#env.action_space.sample()

# %% Train Model using agent/ppo model
"""
    Agent using PPO - multilayer perceptron policy model
"""
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold

save_path = os.path.join('Training','Saved Models')

stop_callback = StopTrainingOnRewardThreshold(reward_threshold=10000,verbose=1)
eval_callback = EvalCallback(env,
                            callback_on_new_best=stop_callback,
                            eval_freq=1000,
                            best_model_save_path=save_path, 
                            verbose=1)

#make multi env 
#from stable_baselines3.common.vec_env import VecFrameStack
env = DummyVecEnv([lambda:CamelotEnv(1000)])
#env = VecFrameStack(env,4) # for multi env


log_path = os.path.join('Training', 'Logs')
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
model.learn(total_timesteps=100000,callback=eval_callback) #callback=eval_callback


"""
PPO overfits in a single environment
requires multiple parallel environments to prevent overfitting
As PPO is an on-policy algorithm it requires multiple parallel environments in 
order to break the correlation between the samples = prevent over fitting.
"""

# %% Save or Load
# load model at path
#model = PPO.load(os.path.join(save_path,'best_model'),env=env) 

# save model at path
#PPO_Path = os.path.join('Training','Saved Models','PPO_400k')
#model.save(PPO_Path) 

#%% Evaluate
evaluate_policy(model,env,n_eval_episodes=5,render=False)
# tensorboard --logdir Training/Logs

# %% Deploy Model in the environment
"""
    Simulation Phase
    Uses trained models in the environment 
"""
from tqdm import tqdm
#del model # delete model
PPO_Path = os.path.join('Training','Saved Models','PPO_400k')
model = PPO.load(PPO_Path,env=env) # load model at path

n = 1000
env = CamelotEnv(n)
#env = DummyVecEnv([lambda:CamelotEnv(1000)])
#env = VecFrameStack(env,4)

mean_score = []
episodes = 10
pbar = tqdm(total=n) if episodes == 1 else None # progress bar

for episode in range(1,episodes+1):
    obs = env.reset() # observation
    done = False
    score = 0
    
    while not done:
        #env.render() #render live
        action,_ = model.predict(obs) #using model
        obs,reward,done,info = env.step(action)
        score += reward
        pbar.update(1) if episodes == 1 else None
    print(f'Episode:{episode} Score:{score}')
    mean_score.append(score)
    #env.render() #render per episode
env.close()
pbar.close() if episodes == 1 else None

print('Total Episodes:{} Average Score:{}'.format(episode, mean(mean_score))) if episode > 1 else None
# %% Plot Mean Scores
import matplotlib.pyplot as plt
plt.hist(mean_score)
# %%
