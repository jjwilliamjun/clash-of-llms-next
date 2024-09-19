"""Definition of the simulation's red team"""
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from class_api.gpt_endpoint import get_message
from excel_api.import_excel import *
from create_node_network.create_network import * 
import create_node_network.create_network as GreenNetwork

class Team:
    def __init__(self, team, model_ID, energy, potency, msg_count, influence_factor, max_cost, temperature, alignment=0):
        """Setting parameters for team"""
        self._team = team
        self._model_ID = model_ID
        self._energy = energy
        self._potency = None
        self._message = None
        self._message_count = msg_count
        self._influence_factor = influence_factor
        self._alignment = alignment
        self._max_cost = max_cost
        self._temperature = temperature
    
    def next_round(self):
        """Increment number of messages sent"""
        self._message_count += 1
    
    def generate_message(self):
        """generate a message with the team's current parameters"""
        self._message, self._potency = get_message(self._team, self._model_ID, self._alignment, self._temperature, self._message_count, self._energy)
        #GreenNetwork.green_team.broadcast_message(self._potency, self._team, self._influence_factor)

    def update_energy_level(self, energy_cost):
        """
        Attempt to generate and send a message. Consumes energy equal to message_cost.
        """
        #End game if energy reaches 0
        if isinstance(energy_cost,float): #Sanitising GPT output
            if self._energy - energy_cost <= 0 :
                self._energy = 0
            else:
                self._energy -= energy_cost
    
    def update_alignment(self, alignment):
        self._alignment = alignment
    
    #TODO potentially bring out to game  parameters
    def energy_cost(self):
        """
        Calculate the energy cost required to send a message based on its potency.

        Parameters:
        - potency (int): The strength of the message (0 to 100).
        - max_cost (int): The max energy cost for the hightest potency (100 potency). 

        Returns:
        - float: The calculated energy cost.
        """
        if isinstance(self._potency, str): 
            return
        if not (0 <= self._potency <= 100):
            raise ValueError("Potency must be between 0 and 100.")
        #TODO more research needed on the way to get energy cost from potency
        energy_cost = self._max_cost * (self._potency / 100)
        return energy_cost
