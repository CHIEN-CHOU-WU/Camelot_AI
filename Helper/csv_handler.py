import csv

def create_item_csv(item_lists):
    with open('csv/items.csv', encoding='utf-8-sig', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Item name', 'Count', 'HP Effect', 'Hunger Effect ', 'Position'])
        for item in item_lists:
            csv_writer.writerow([item.name, item.count, item.hp_effect, item.hunger_effect, item.position])

def update_item_csv(item_lists):
    with open('csv/items.csv', encoding='utf-8-sig', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Item name', 'Count', 'HP Effect', 'Hunger Effect ', 'Position'])
        for item in item_lists:
            csv_writer.writerow([item.name, item.count, item.hp_effect, item.hunger_effect, item.position])

def create_state_csv(state):
    with open('csv/state.csv', encoding='utf-8-sig', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(state.keys())
        csv_writer.writerow(state.values())

def update_state_csv(state):
    # Add hunger and health state to state.csv
    with open('csv/state.csv', encoding='utf-8-sig', mode='a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(state.values())

def store_observation_csv(state):
     with open('csv/observation.csv', encoding='utf-8-sig', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(state.keys())
        csv_writer.writerow(state.values())

def clear_observation_csv():
    csv_file =  open('../csv/observation.csv', encoding='utf-8-sig', mode='w+')
    csv_file.close()

def store_action_csv(action, state):
     with open('../csv/action.csv', encoding='utf-8-sig', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(action)
        csv_writer.writerow(state)
    
def clear_action_csv():
    csv_file =  open('csv/action.csv', encoding='utf-8-sig', mode='w+')
    csv_file.close()

def get_action_csv():
    with open('csv/action.csv', encoding='utf-8-sig', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        actions = []
        for row in csv_reader:
            [actions.append(int(i)) for i in row]
        
        state = {
            'hunger': actions[1],
            'energy': actions[2],
            'health': actions[3]
        }   

        return actions[0], state