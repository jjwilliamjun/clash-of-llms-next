class Blue_agent: 
    def __init__(self, ai_name, influence_factor, initial_energy, num_msg_sent):
        self.name = ai_name
        self.influence_factor = influence_factor
        self.energy_level = initial_energy
        self.num_msg_sent = 0
        

    def update_energy_level(self, energy_cost):
        """
        Attempt to generate and send a message. Consumes energy equal to message_cost.
        """
        
        if self.energy_level - energy_cost <= 0 :
            print(f"{self.name} cannot send the message")
        else:
            print(f"{self.name} can send the message")
            self.energy_level - energy_cost
    def gen_msg():
        """
        Generate a message using chatgpt
        """
        pass
    def send_msg():
        """
        Send the message and consume energy
        """
        pass
