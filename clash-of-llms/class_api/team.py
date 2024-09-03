"""Definition of the simulation's red team"""
from gpt_endpoint import get_message

class Team:
    def __init__(self, team, model_ID, energy, influence_factor, max_cost, temperature, alignment=0):
        """Setting parameters for team"""
        self._team = team
        self._model_ID = model_ID
        self._energy = energy
        self._potency = None
        self._message = None
        self._message_count = 0
        self._influence_factor = influence_factor
        self._alignment = alignment
        self._max_cost = max_cost
        self._temperature = temperature
    
    def next_round(self):
        """Increment number of messages sent"""
        self._message_count += 1
    
    def generate_message(self):
        """generate a message with the team's current parameters"""
        self._message, self._potency = get_message(self._team, self._alignment, self._energy)

    def update_energy_level(self, energy_cost):
        """Consumes energy equal to message_cost"""
        if self._energy - energy_cost <= 0 :
            self._energy = 0
        else:
            self._energy -= energy_cost

    #TODO potentially bring out to game parameters
    def energy_cost(self):
        """Calculate the energy cost required to send a message based on its potency"""

        if not (0 <= self._potency <= 100):
            raise ValueError("Potency must be between 0 and 100.")
        #TODO more research needed on the way to get energy cost from potency
        energy_cost = self._max_cost * (self._potency / 100)
        return energy_cost
