"""Simulation class"""
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from create_node_network.green_team import GreenTeam
from excel_api.game_data import GameTurnData
from class_api.team import Team, BlueTeam, RedTeam


class Simulation:
    """The main simulation loop"""
    def __init__(self, red_team: RedTeam, blue_team: BlueTeam, green_team: GreenTeam, topic: str):
        """Initialization"""
        self._red_team= red_team
        self._blue_team = blue_team
        # self._round_num = 0
        self._victor = None
        # self._green_team = create_node_network(node_attributes, node_connec)
        self._green_team = green_team
        self._msg_content = []
        self._current_team = 'red'
        self._topic = topic
        self._termination_reason = None

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
            self._red_team.generate_message(topic = self._topic)
            self._green_team.broadcast_message(self._red_team._potency, self._red_team, self._red_team._influence_factor)
            self._green_team.update_green_network()

            # Update alignments for red and blue teams
            self._red_team.update_alignment(round(self._green_team.red_alignment(), 2))
            self._blue_team.update_alignment(round(self._green_team.blue_alignment(), 2))

            # Blue team generates a message and updates energy
            self._blue_team.generate_message(topic = self._topic)
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
    
    
    def next_round(self, terminating_conditions):
        """Run Simulation"""

        if self._victor is not None:
            return self._victor, self._termination_reason
        
        # Energy depletion
        if self._blue_team._energy == 0:
            self._victor = 'red'
            self._termination_reason = "Blue team energy depletion"
            return self._victor, self._termination_reason

        # Population majority
        if self._red_team._alignment >= terminating_conditions._alignment:
            self._victor = 'red'
            self._termination_reason = "Majority support for red team"
            return self._victor, self._termination_reason
        
        elif self._blue_team._alignment >= terminating_conditions._alignment:
            self._victor = "blue"
            self._termination_reason = "Majority support for blue team"
            return self._victor, self._termination_reason
        
        # Agents perform turn actions
        if self._current_team == 'red':
            self._red_team.generate_message(topic=self._topic, previous="")
            # self._red_team.apply_penalty()
            if(not isinstance(self._red_team._potency,str)):
                self._green_team.broadcast_message(self._red_team,self._red_team._potency, self._red_team, self._red_team._influence_factor)
                self._green_team.update_green_network()
            print("updated")
            
        elif self._current_team == 'blue':
            self._blue_team.generate_message(topic=self._topic, previous=self._red_team._message)
            if(not isinstance(self._blue_team._potency,str)):
                self._green_team.broadcast_message(self._red_team,self._blue_team._potency, self._blue_team, self._blue_team._influence_factor)
                self._green_team.update_green_network()
            energy_cost=self._blue_team.energy_cost()
            self._blue_team.update_energy_level(energy_cost)
        

        # Update alignments for red and blue teams
        self._red_team.update_alignment(round(self._green_team.red_alignment(), 2))
        self._blue_team.update_alignment(round(self._green_team.blue_alignment(), 2))
        
        # End Simulation
        return self._victor, self._termination_reason
    
    def switch_teams(self):
        """Switch current team for next round"""
        if self._current_team == 'red':
            self._current_team = 'blue'
        else:
            self._current_team = 'red'
    
    def get_turn_data(self, round_num) -> GameTurnData:
        """Returns a GameTurnData object for last turn"""
        turn_data = GameTurnData()

        if self._current_team == 'red':
            turn_data.set_all_turn_data(
                turn=round_num,
                team=self._red_team._team,
                message_chosen=self._red_team._message,
                potency=self._red_team._potency,
                energy_level="NA",
                red_alignment=self._red_team._alignment,
                blue_alignment=self._blue_team._alignment
            )

        elif self._current_team == 'blue':
            turn_data.set_all_turn_data(
                turn=round_num,
                team=self._blue_team._team,
                message_chosen=self._blue_team._message,
                potency=self._blue_team._potency,
                energy_level=self._blue_team._energy,
                red_alignment=self._red_team._alignment,
                blue_alignment=self._blue_team._alignment
            )
        
        # End Simulation
        return turn_data
    
