"""Simulation class"""
import os
import sys
# Attempt the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from excel_api.create_node_network.create_network import create_node_network
from team import Team


class Simulation:
    """The main simulation loop"""
    def __init__(self, red_team_param, blue_team_param, node_attributes, node_connec):
        """Initialization"""
        self._red_team= Team(**red_team_param)
        self._blue_team = Team(**blue_team_param)
        self._round_num = 1
        self._victor = None
        create_node_network(node_attributes, node_connec)

    def start(self):
        """Run Simulation"""
        while True:
            # TODO Receive and examine data from front end
            
            # Energy depletion
            if self._blue_team._energy == 0:
                self._victor = 'red'
                print("Blue Team has run out of energy")
                break
            
            # Population majority
            # TODO Potentially returned from the frontend
            if self._red_team._alignment >= 80:
                self._victor = 'red'
                print("Red Team has gained majority support")
                break
            elif self._blue_team._alignment >= 80:
                self._victor = "blue"
                print("Blue Team has gained majority support")
                break
            
            print(f"--- Round {self._round_num} ---")

            # Red team generates a message and updates energy
            self._red_team.generate_message()


            # Blue team generates a message and updates energy
            self._blue_team.generate_message()
            blue_energy_cost = self._blue_team.energy_cost()
            self._blue_team.update_energy_level(blue_energy_cost)

            # Move to the next round
            self._red_team.next_round()
            self._blue_team.next_round()

            self._round_num += 1

        if self._victor == 'red':
            print("🔴 Red Team Wins")
        else:
            print("🔵 Blue Team Wins")
        
        # End Simulation
        print("Simulation finished.")
        return self._victor