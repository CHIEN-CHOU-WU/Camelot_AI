#%% Imports
import os
import time
import pandas as pd
import random
import sys
import threading

from stable_baselines3 import PPO
from action import action
from Actions.set_positions import set_character_position, set_item_position
from Entities.characters import Characters
from Entities.items import Items

class CamelotEnv:
    def __init__(self, dev='') -> None:
        self.dev = dev
        if self.dev != 'dev':
            self.setup_env()
            self.setup_items()
            self.setup_state()
            self.setup_camera()
            self.main()
        else:
            self.setup_items()
            self.setup_state()
            # 建立一個子執行緒
            t = threading.Thread(target = self.camelot_input)
            # 執行該子執行緒
            t.start()
            self.dev_mode()
            # 等待 t 這個子執行緒結束
            t.join()
            print("Done.")

    def camelot_input(self):
        self.result = ''
        while self.result != 'input Quit':
            self.result = input()
            print('result', self.result)
            time.sleep(1)

    def setup_env(self):
        action('CreatePlace(Tavern, Tavern)')                       # Setup place
        self.kate = Characters('Kate', 'C', 'Long', 'Queen')        # Setup character
        set_character_position('Kate', 'Tavern.Door')               # Setup character position

    def setup_items(self):
        self.surfaces = ['Tavern.Table.Left', 'Tavern.Table.Right', 'Tavern.Table.FrontLeft', 'Tavern.Table.BackLeft']
        random.shuffle(self.surfaces)

        # Items :          ( name,        item_type,  effect, count,   position, hp_effect, hunger_effect)
        self.apple_list = [Items('poison_apple', 'Apple', 'Poison', 10, self.surfaces.pop(), -10, -5),
                           Items('magic_apple', 'Apple', 'Magic', 10, self.surfaces.pop(), 10, -3),
                           Items('force_apple', 'Apple', 'Force', 10, self.surfaces.pop(), 1, -1),
                           Items('heart_apple', 'Apple', 'Heart', 10, self.surfaces.pop(), 15, -2)]

        apples_name = []
        apples_effect = []
        apples_count = []
        apples_position = []
        apples_hp_effect = []
        apples_hunger_effect = []

        for apple in self.apple_list:
            apples_name.append(apple.name)
            apples_effect.append(apple.effect)
            apples_count.append(apple.count)
            apples_position.append(apple.position)
            apples_hp_effect.append(apple.hp_effect)
            apples_hunger_effect.append(apple.hunger_effect)


        self.apple_df = pd.DataFrame({"name": apples_name,
                                      "effect": apples_effect,
                                      "count": apples_count,
                                      "position": apples_position,
                                      "hp_effect": apples_hp_effect,
                                      "hunger_effect": apples_hunger_effect})

        self.apple_df.to_csv('csv/items.csv', index=False)

        if self.dev != 'dev':
            for apple in self.apple_list:
                set_item_position(apple.name, apple.item_type, apple.position, effect=apple.effect)

    def setup_state(self):
        self.alive = True
        self.start_time = 1
        self.interval = 3000

        # initialize predict_flag.csv
        predict_flag = pd.DataFrame({'Flag':[False]})
        predict_flag.to_csv('csv/predict_flag.csv', index=False)

        # initialize state.csv & observation.csv
        state_history = pd.DataFrame([[0, 100, 100, -1]], columns = ["hunger", "energy", "health", "action"])
        state_history.to_csv('csv/observation.csv', index=False)
        state_history.to_csv('csv/state.csv', index=False)
        

    def setup_camera(self):
        action('SetCameraFocus(Kate)')
        action('ShowMenu()')
        action('SetTitle(Camelot World)')
        action('HideMenu()')
        action('EnableInput()')

    def dev_mode(self):
        print('Testing environment')
        try:
            self.main()
        except KeyboardInterrupt:
            print('em.py interrupted!')

    def main(self):
        while self.alive:
            # every 3 seconds
            if time.time() - self.start_time >= int(self.interval/1000):
                predict_flag = pd.read_csv('csv/predict_flag.csv').iloc[0][0]
                if predict_flag == False:
                    self.action = pd.read_csv('csv/observation.csv').iloc[0][-1]

                    if self.dev != 'dev':
                        # action in Camelot
                        if self.action == 0 or self.action == 1 or self.action == 2 or self.action == 3:
                            apple = self.apple_list[self.action]
                            self.kate.take(apple.name, apple.position)
                            self.kate.drink()
                        if self.action == 4:
                            self.kate.sleep('Tavern.Chair')
                        if self.action == 5:
                            self.kate.wave()
                            
                    # update predict_flag.csv
                    predict_flag = pd.DataFrame({'Flag':[True]})
                    predict_flag.to_csv('csv/predict_flag.csv', index=False)

                    # itmes control
                    if self.action == 0 or self.action == 1 or self.action == 2 or self.action == 3:
                        self.apple_df.loc[self.action, 'count'] -= 1

                        self.apple_df.to_csv('csv/items.csv', index=False)


                # reset time
                self.start_time = time.time()
        

if __name__ == "__main__":
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    try:    # develop mode
        dev = args[0]
        camelot_env = CamelotEnv(dev = dev)
    except: # Camelot
        camelot_env = CamelotEnv()
        
