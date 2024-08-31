
from team import Team


class simulation:
    """The main simulation loop"""
    def __init__(self, red_team_param, blue_team_param):
        """Initialize the simulation with one Red team and one Blue team."""
        self.red_team= Team(**red_team_param)
        self.blue_team = Team(**blue_team_param)
        pass
    def running(self):
        """
        Run the simulation, which could involve multiple rounds.
        """
        round_number = 1
        while self.blue_team._energy > 0:
            print(f"--- Round {round_number} ---")

            # Red team generates a message and updates energy
            self.red_team.generate_message()


            # Blue team generates a message and updates energy
            self.blue_team.generate_message()
            blue_energy_cost = self.blue_team.energy_cost()
            self.blue_team.update_energy_level(blue_energy_cost)

            # Move to the next round
            self.red_team.next_round()
            self.blue_team.next_round()

            round_number += 1

        print("Simulation finished.")

# Example usage:
red_team_params = {
    'team': 'Red',
    'model_ID': 'model_red',
    'energy': 0,
    'influence_factor': 10,
    'max_cost': 20,
    'alignment': 0
}

blue_team_params = {
    'team': 'Blue',
    'model_ID': 'model_blue',
    'energy': 50,
    'influence_factor': 12,
    'max_cost': 20,
    'alignment': 1
}

simulation = simulation(red_team_params, blue_team_params)
simulation.running()