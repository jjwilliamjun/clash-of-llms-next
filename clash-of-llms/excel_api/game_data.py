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
        self.increased_alignment = None
        self.decreased_alignment = None

    def set_turn(self, turn):
        """Setting turn to self"""
        self.turn = turn

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

    def set_increased_alignment(self, increased_alignment):
        """increase in alignment"""
        self.increased_alignment = increased_alignment

    def set_decreased_alignment(self, decreased_alignment):
        """decrease in alignment"""
        self.decreased_alignment = decreased_alignment

    def get_turn_data(self):
        """Data associated with the turn"""
        return {
            'Turn': self.turn, 
            'Team': self.team, 
            'Message chosen': self.message_chosen, 
            'Potency of message': self.potency, 
            'Energy level': self.energy_level, 
            '% of nodes with increased alignment towards team': self.increased_alignment, 
            '% of nodes with decreased alignment towards team': self.decreased_alignment
        }
