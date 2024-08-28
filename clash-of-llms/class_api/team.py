"""Definition of the simulation's red team"""
from gpt_endpoint import get_message

class team:
    def __init__(self, team, model_ID, energy=0, potency, influence_factor, max_cost, alignment=0):
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
    
    def next_round(self):
        """Increment number of messages sent"""
        self._message_count += 1
    
    def generate_message(self):
        """generate a message with the team's current parameters"""
        self._message, self._potency = get_message(self._team, self._alignment, self._energy)
        
    def update_energy_level(self, energy_cost):
        """
        Attempt to generate and send a message. Consumes energy equal to message_cost.
        """
        
        if self._energy - energy_cost <= 0 :
            print(f"{self._team} cannot send the message")
        else:
            print(f"{self._team} can send the message")
            self._energy -= energy_cost

    #TODO potentially bring out to game parameters
    def energy_cost(self):
        """
        Calculate the energy cost required to send a message based on its potency.

        Parameters:
        - potency (int): The strength of the message (0 to 100).
        - max_cost (int): The max energy cost for the hightest potency (100 potency). 

        Returns:
        - float: The calculated energy cost.
        """

        if not (0 <= self._potency <= 100):
            raise ValueError("Potency must be between 0 and 100.")
        #TODO more research needed on the way to get energy cost from potency
        energy_cost = self._max_cost * (self._potency / 100)
        return energy_cost
