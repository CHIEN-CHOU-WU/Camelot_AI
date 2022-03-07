#%%
import time
import random
import os
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import HORIZONTAL, Label, StringVar
from action import action
from Actions.set_positions import set_character_position, set_item_position
from Entities.characters import Characters
from Entities.items import Items
from Helper.csv_handler import create_item_csv, create_state_csv, update_state_csv, update_item_csv, store_observation_csv, clear_action_csv, get_action_csv
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.ttk import Combobox, Separator
from pandastable import Table
from Model.camelot_predicting import predict_action


#%% Setup
# 1. Set up place
# 2. Set up characters and their position
# 3. Set up items and positions
# 4. Set up State
# 5. Focus on Kate
# 6. tkinter

# # 1. Set up place
# action('CreatePlace(Tavern, Tavern)')

# # 2. Set up characters and their position
# kate = Characters('Kate', 'C', 'Long', 'Queen')
# set_character_position('Kate', 'Tavern.Door')
# # bob = Characters('Bob', 'F', 'Mage_Full', 'Peasant')
# # set_character_position('Bob', 'Shop.Chest')

# # 3. Set up items and positions
# # surface
# surfaces = ['Tavern.Table.Left', 'Tavern.Table.Right', 'Tavern.Table.FrontLeft', 'Tavern.Table.BackLeft']
# random.shuffle(surfaces)

# # Items :          ( name,        item_type,  effect, count,   position, hp_effect, hunger_effect)
# apple_list = [Items('poison_apple', 'Apple', 'Poison', 2, surfaces.pop(), -10, -5),
#               Items('magic_apple', 'Apple', 'Magic', 2, surfaces.pop(), 10, -3),
#               Items('force_apple', 'Apple', 'Force', 2, surfaces.pop(), 1, -1),
#               Items('heart_apple', 'Apple', 'Heart', 2, surfaces.pop(), 15, -2)]

# for apple in apple_list:
#     set_item_position(apple.name, apple.item_type, apple.position, effect=apple.effect)

# 4. Set up State
hunger = 0
energy = 100
health = 100
alive = True
obs = (hunger, energy, health)
state_history = pd.DataFrame([[hunger, energy, health]], columns = ["hunger", "energy", "health"])

def get_action_meanings():
        return {0: "Eat poison apple",
                1: "Eat magic apple",
                2: "Eat force apple",
                3: "Eat heart apple",
                4: "Sleep",
                5: "Wave"}

# # 5. Focus on Kate
# action('SetCameraFocus(Kate)')

# # Focus on Tavern Door
# # action('SetCameraFocus(Tavern.FrontLeftStool)')
# # action('SetCameraMode(track)')

# # Show Menu, set title, inable input
# action('ShowMenu()')
# action('SetTitle(Camelot World)')
# action('HideMenu()')

# action('EnableInput()')

# 6. tkinter
window = tk.Tk()

window.title("Camelot DashBoard")

window.geometry('900x700')

# Character state
lbl = Label(window, text="Character state")

lbl.grid(column=0, row=0, columnspan=2)

#%% Chart plot
figure = plt.Figure(figsize=(5,4), dpi=100)
ax1 = figure.add_subplot(111)
line = FigureCanvasTkAgg(figure, window)
line.get_tk_widget().grid(column=0, row=1)

def animate(i, state_history):
    # data = pd.read_csv('csv/state.csv')
    data = state_history
    print(state_history)
    xs = []
    ys_hunger = []
    ys_energy = []
    ys_health = []
    for index, row in data.iterrows():
        y_hunger = row.hunger
        y_energy = row.energy
        y_health = row.health
        xs.append(int(index))
        ys_hunger.append(int(y_hunger))
        ys_energy.append(int(y_energy))
        ys_health.append(int(y_health))
    ax1.clear()
    ax1.plot(xs, ys_hunger, label='hunger')
    ax1.plot(xs, ys_energy, label='energy')
    ax1.plot(xs, ys_health, label='health')
    ax1.legend()

ani = animation.FuncAnimation(figure, animate, interval=1000)

#%% Character table
frame =tk.Frame(window)
frame.grid(column=1, row=1)

state_table = Table(frame, width=380)
state_table.show()

def state_update(state_history):
    state_table.redraw()
    # state_table.model.df = pd.read_csv('csv/state.csv', header=0).iloc[::-1]
    state_table.model.df = state_history
    state_table.autoResizeColumns()
    # window.after(500, state_update) # run itself again after 500 ms

def main(obs, alive, state_history):
    if alive:
        # predict action via RL
        action, obs, reward, done, info = predict_action(obs)

        obs_series = pd.DataFrame([obs], columns = ["hunger", "energy", "health"])
        state_history = pd.concat([state_history, obs_series])
        state_update(state_history)

        # # act
        # if action == 0 or action == 1 or action == 2 or action == 3:
        #     apple = apple_list[action]
        #     kate.take(apple.name, apple.position)
        #     kate.drink()
        # if action == 4:
        #     kate.sleep('Tavern.Chair')
        # if action == 5:
        #     kate.wave()

        # # if health <= 0
        # if obs[-1] <= 0:
        #     kate.die()
        #     alive = False

        window.after(5000, main, obs, alive, state_history) # run itself again after 5 sec

main(obs, alive, state_history)

window.mainloop()