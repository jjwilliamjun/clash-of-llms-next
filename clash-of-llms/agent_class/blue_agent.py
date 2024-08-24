class Blue_agent: 
    def __init__(self, ai_name, influence_factor, initial_energy, num_msg_gen):
        self.name = ai_name
        self.influence_factor = influence_factor
        self.energy_level = initial_energy
        self.num_msg_gen = num_msg_gen

    def update_energy_level(self, energy_deducted):
        new_energy_level = self.energy_level - energy_deducted
        if new_energy_level <= 0 :
            return 0
        else:
            return new_energy_level

