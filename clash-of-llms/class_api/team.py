"""Definition of the simulation's red team"""
from gpt_endpoint import get_message

class team:
    def __init__(self, model_ID, energy, potency, influence_factor, alignment=0):
        """Setting parameters for red team"""
        self._team = 'red'
        self._energy = energy
        self._model_ID = model_ID
        self._potency = potency
        self._message_count = 0
        self._influence_factor = influence_factor
        self._alignment = alignment
        
    def team(self):
        """Get the team name"""
        return self._team
    
    def next_round(self):
        """Increment number of messages sent"""
        self._message_count += 1
        
    def set_potency(self, potency):
        """set potency of message"""
        self._potency = potency
    
    def generate_message(self):
        """generate a message with the team's current parameters"""
        message = get_message(self._team, self._alignment, self._energy)
        return message
    def update_energy_level(self, energy_cost):
        """
        Attempt to generate and send a message. Consumes energy equal to message_cost.
        """
        
        if self._energy - energy_cost <= 0 :
            print(f"{self._team} cannot send the message")
        else:
            print(f"{self._team} can send the message")
            self._energy - energy_cost