"Tests for simulation"
import unittest
from simulation import Simulation
from excel_api.import_excel import import_node_attributes, import_node_connections

red_team_params = {
    'team': 'Red',
    'model_ID': 'model_red',
    'energy': 0,
    'influence_factor': 10,
    'max_cost': 20,
    'alignment': 40
}

blue_team_params = {
    'team': 'Blue',
    'model_ID': 'model_blue',
    'energy': 100,
    'influence_factor': 12,
    'max_cost': 20,
    'alignment': 60
}

class TestSimulation(unittest.TestCase):
    def test_initialization(self):
        """Simulate running test"""
        node_attributes = import_node_attributes('NodeAttributes.xlsx')
        node_connections = import_node_connections('NodeConnections.xlsx')
        sim = Simulation(red_team_params, blue_team_params, node_attributes, node_connections)
        victor = sim.start()
        self.assertEqual(victor, 'red')
            

if __name__ == "__main__":
    unittest.main()
