#%%
import time
import random
import os
from action import action
from Actions.set_positions import set_character_position, set_item_position
from Entities.characters import Characters
from Entities.items import Items
from Helper.csv_handler import create_item_csv, create_state_csv, update_state_csv, update_item_csv, store_observation_csv, clear_action_csv, get_action_csv
# import matplotlib

#%% Setup
# 1. Set up place
# 2. Set up characters and their position
# 3. Set up items and positions
# 4. Set up State
# 5. Focus on Kate

# 1. Set up place
action('CreatePlace(Tavern, Tavern)')

# 2. Set up characters and their position
kate = Characters('Kate', 'C', 'Long', 'Queen')
set_character_position('Kate', 'Tavern.Door')
# bob = Characters('Bob', 'F', 'Mage_Full', 'Peasant')
# set_character_position('Bob', 'Shop.Chest')

# 3. Set up items and positions
# surface
surfaces = ['Tavern.Table.Left', 'Tavern.Table.Right', 'Tavern.Table.FrontLeft', 'Tavern.Table.BackLeft']
random.shuffle(surfaces)

# Items :          ( name,        item_type,  effect, count,   position, hp_effect, hunger_effect)
apple_list = [Items('poison_apple', 'Apple', 'Poison', 2, surfaces.pop(), -10, -5),
              Items('magic_apple', 'Apple', 'Magic', 2, surfaces.pop(), 10, -3),
              Items('force_apple', 'Apple', 'Force', 2, surfaces.pop(), 1, -1),
              Items('heart_apple', 'Apple', 'Heart', 2, surfaces.pop(), 15, -2)]

for apple in apple_list:
    set_item_position(apple.name, apple.item_type, apple.position, effect=apple.effect)

# 4. Set up State
hunger = 0
energy = 100
health = 100
state = {
    'hunger': hunger,
    'energy': energy,
    'health': health
}
def get_action_meanings():
        return {0: "Eat poison apple",
                1: "Eat magic apple",
                2: "Eat force apple",
                3: "Eat heart apple",
                4: "Sleep",
                5: "Wave"}
alive = True
start = 1       # Time

# 5. Focus on Kate
action('SetCameraFocus(Kate)')

# Focus on Tavern Door
# action('SetCameraFocus(Tavern.FrontLeftStool)')
# action('SetCameraMode(track)')

#%% Show Menu, set title, inable input
action('ShowMenu()')
action('SetTitle(Camelot World)')
action('HideMenu()')

action('EnableInput()')

#%% Create CSV file
# items.csv
create_item_csv(apple_list)

# state.csv & observation.csv
state_with_action = state.copy()
state_with_action['action'] = -1
create_state_csv(state_with_action)
store_observation_csv(state)

# Respond to input.
while(True):
    # kate.sit('Tavern.FrontLeftStool')

    if alive:
        # if action.csv exists and is empty
        if os.path.exists("csv/action.csv") and os.stat("csv/action.csv").st_size != 0:
            # Every 1 secalive = False
            if time.time() - start >= 5:

                # get action and observation
                action, state = get_action_csv()
                state_with_action = state.copy()
                state_with_action['action'] = get_action_meanings()[action]

                # act
                if action == 0 or action == 1 or action == 2 or action == 3:
                    apple = apple_list[action]
                    kate.take(apple.name, apple.position)
                    kate.drink()
                if action == 4:
                    kate.sleep('Tavern.Chair')
                if action == 5:
                    kate.wave()

                # update state and store observation to csv file
                update_state_csv(state_with_action)
                store_observation_csv(state)

                # clear action
                clear_action_csv()

                start = time.time()

        if state['health'] <= 0:
            kate.die()
            alive = False
    else:
        break
        

    # i = input()