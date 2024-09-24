"""Usage:
- Initialize GameData instance per simulation
- Initialize GameTurnData instance per turn in simulation. 
Must call add_entry to at the end of the simulation"""

class GameData:
    """Object with game data"""
    def __init__(self):
        """initialisation"""
        self.data = []

    def add_entry(self, simulation_data_obj):
        """New entry"""
        self.data.append(simulation_data_obj.get_turn_data())

    def get_results(self):
        """returning result"""
        return self.data
class GameTurnData:
    """Object with game turn data"""
    def __init__(self):
        """initialisation"""
        self.turn = None
        self.team = None
        self.message_chosen = None
        self.potency = None
        self.energy_level = None
        self.red_alignment = None
        self.blue_alignment = None

    def set_turn(self, turn):
        """Setting turn to self"""
        self.turn = turn
    def set_all_turn_data(self, turn, team, message_chosen, potency, energy_level, red_alignment, blue_alignment):
        self.set_turn(turn)
        self.set_team(team)
        self.set_message_chosen(message_chosen)
        self.set_potency(potency)
        self.set_energy_level(energy_level)
        self.set_red_alignment(red_alignment)
        self.set_blue_alignment(blue_alignment)
        
    def set_team(self, team):
        """Setting team"""
        self.team = team

    def set_message_chosen(self, message):
        """Choosing message"""
        self.message_chosen = message

    def set_potency(self, potency):
        """potency if msg"""
        self.potency = potency

    def set_energy_level(self, energy_level):
        """Energy level"""
        self.energy_level = energy_level

    def set_red_alignment(self, red_alignment):
        """increase in alignment"""
        self.red_alignment = red_alignment

    def set_blue_alignment(self, blue_alignment):
        """decrease in alignment"""
        self.blue_alignment = blue_alignment

    def get_turn_data(self):
        """Data associated with the turn"""
        return {
            'Turn': self.turn, 
            'Team': self.team, 
            'Message chosen': self.message_chosen, 
            'Potency of message': self.potency, 
            'Energy level': self.energy_level, 
            '% of nodes red-aligned': self.red_alignment, 
            '% of nodes blue_aligned': self.blue_alignment
        }
