# Initialization and population of global game_data
from game_data import *
# Create the GameData instance
game_data = GameData()

# Create and populate GameTurnData instances
turn_data_1 = GameTurnData()
turn_data_1.set_turn(1)
turn_data_1.set_team('Blue')
turn_data_1.set_message_chosen('Message is true')
turn_data_1.set_potency(0.8)
turn_data_1.set_energy_level(80)
turn_data_1.set_increased_alignment(60)

# Add the populated turn_data_1 to game_data
game_data.add_entry(turn_data_1)

# Create and populate another GameTurnData instance
turn_data_2 = GameTurnData()
turn_data_2.set_turn(2)
turn_data_2.set_team('Red')
turn_data_2.set_message_chosen('Message is false')
turn_data_2.set_potency(0.6)
turn_data_2.set_energy_level(70)
turn_data_2.set_increased_alignment(40)
turn_data_2.set_decreased_alignment(10)

# Add the populated turn_data_2 to game_data
game_data.add_entry(turn_data_2)
print(game_data)
# The global game_data variable is now populated with test data
