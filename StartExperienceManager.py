from action import action
from Actions.set_positions import set_character_position, set_item_position
from Entities.characters import Characters
import numpy as np
import threading
import time
# from IPython import display
# import matplotlib.pyplot as plt
# from State.character_state import character_state

# Set up place
action('CreatePlace(Shop, AlchemyShop)')

# Set up items
set_item_position('rotten_apple','Apple', 'Shop.Table.Left', effect='Poison')

# Set up characters and their position
bob = Characters('Bob', 'F', 'Mage_Full', 'Peasant')
kate = Characters('Kate', 'C', 'Long', 'Queen')

set_character_position('Bob', 'Shop.Chest')
set_character_position('Kate', 'Bob')

# Show Menu and set title
action('ShowMenu()')
action('SetTitle(Camelot World)')

hunger = 100
start = -1
def hunger_state(hunger):
	hunger -= 1
	return hunger

# Respond to input.
while(True):

	i = input()
	if start > 0 and (time.time()-start)>2:
		hunger = hunger_state(hunger)
		start = time.time()
	# Action
	# hunger = hunger_state(hunger)
	# if hunger == 98:
		# action('SetNarration("'+str(hunger)+'")')
		# action('ShowNarration()')
		kate.take('rotten_apple', 'Shop.Table.Left')
		kate.give('rotten_apple', 'Bob')
		action('Drink(Bob)')
		# bob.die()

	# Menu
	if(i == 'input Selected Start'):
		action('SetCameraFocus(Kate)')
		action('HideMenu()')
		action('EnableInput()')
		start = time.time()
	
	# if(i == 'input Key Pause'):

	if(i == 'input Key Interact'):
		action('Attack(Kate, Bob, true)')

	if(i == 'input Selected Credits'):
		action('ShowCredits()')
	if(i == 'input Close Credits'):
		action('HideCredits()')
	if(i == 'input Selected Quit'):
		action('Quit()')
	if(i == 'input Open_Door BobsHouse.Door'):
		action('SetNarration("The door is locked!")')
		action('ShowNarration()')
	if(i == 'input Close Narration'):
		action('HideNarration()')

	if(i == 'input Key Inventory'):
		action('ShowList(Kate)')
		
	if(i =='input Close List'):
		action('HideList()')