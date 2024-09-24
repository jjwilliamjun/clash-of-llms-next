"""Simulation class"""
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from create_node_network.green_team import GreenTeam
from excel_api.game_data import GameTurnData
from class_api.team import Team


class Simulation:
    """The main simulation loop"""
    def __init__(self, red_team: Team, blue_team: Team, green_team: GreenTeam):
        """Initialization"""
        self._red_team= red_team
        self._blue_team = blue_team
        self._round_num = 0
        self._victor = None
        # self._green_team = create_node_network(node_attributes, node_connec)
        self._green_team = green_team
        self._turn_data = GameTurnData()
        self._msg_content = []
        self._current_team = 'red'

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
            self._green_team.broadcast_message(self._red_team._potency, self._red_team, self._red_team._influence_factor)
            self._green_team.update_green_network()

            # Update alignments for red and blue teams
            self._red_team.update_alignment(round(self._green_team.red_alignment(), 2))
            self._blue_team.update_alignment(round(self._green_team.blue_alignment(), 2))

            # Blue team generates a message and updates energy
            self._blue_team.generate_message()
            self._green_team.broadcast_message(self._blue_team._potency, self._blue_team, self._blue_team._influence_factor)
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
    
    
    def next_round(self):
        """Run Simulation"""

        # Energy depletion
        if self._blue_team._energy == 0:
            self._victor = 'red'
            print("Blue Team has run out of energy")
            return self._victor

        # Population majority
        # TODO Potentially returned from the frontend
        if self._red_team._alignment >= 80 or self._blue_team._alignment < 1:
            self._victor = 'red'
            print("Red Team has gained majority support")
            return self._victor
        
        elif self._blue_team._alignment >= 80 or self._blue_team._alignment < 1:
            self._victor = "blue"
            print("Blue Team has gained majority support")
            return self._victor
        
        if self._current_team == 'red':
            self._red_team.generate_message()
            self._red_team.apply_penalty()
            if(not isinstance(self._red_team._potency,str)):
                self._green_team.broadcast_message(self._red_team._potency, self._red_team, self._red_team._influence_factor)
                self._green_team.update_green_network()

        elif self._current_team == 'blue':
            self._blue_team.generate_message()
            if(not isinstance(self._blue_team._potency,str)):
                self._green_team.broadcast_message(self._blue_team._potency, self._blue_team, self._blue_team._influence_factor)
                self._green_team.update_green_network()
            energy_cost=self._blue_team.energy_cost()
            self._blue_team.update_energy_level(energy_cost)
            

        # Update alignments for red and blue teams
        self._red_team.update_alignment(round(self._green_team.red_alignment(), 2))
        self._blue_team.update_alignment(round(self._green_team.blue_alignment(), 2))

        if self._current_team == 'red':
            # Update turn data        
            self._turn_data.set_all_turn_data(
                turn=self._round_num,
                team=self._red_team,
                message_chosen=self._red_team._message,
                potency=self._red_team._potency,
                energy_level=self._red_team._energy,
                red_alignment=self._red_team._alignment,
                blue_alignment=self._blue_team._alignment
            )

        elif self._current_team == 'blue':
            # Update turn data        
            self._turn_data.set_all_turn_data(
                turn=self._round_num,
                team=self._blue_team,
                message_chosen=self._blue_team._message,
                potency=self._blue_team._potency,
                energy_level=self._blue_team._energy,
                red_alignment=self._red_team._alignment,
                blue_alignment=self._blue_team._alignment
            )

        # Move to the next round
        self._red_team.next_round()
        self._blue_team.next_round()
        self._round_num += 1
        
        # End Simulation
        return self._victor
    
    def switch_teams(self):
        """Switch current team for next round"""
        if self._current_team == 'red':
            self._current_team = 'blue'
        else:
            self._current_team = 'red'