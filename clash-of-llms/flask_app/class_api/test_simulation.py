"Tests for simulation"
import unittest
import os
import sys
from simulation import Simulation

# Add the parent directory of class_api to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from excel_api.import_excel import import_node_attributes, import_node_connections

red_team_params = {
    'team': 'Red',
    'model_ID': 'model_red',
    'energy': 0,
    'influence_factor': 10,
    'max_cost': 20,
    'temperature': 0.5,
    'alignment': 40
}

blue_team_params = {
    'team': 'Blue',
    'model_ID': 'model_blue',
    'energy': 100,
    'influence_factor': 12,
    'max_cost': 20,
    'temperature': 0.5,
    'alignment': 60
}

class TestSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup any state before running the tests"""
        # Load node attributes and connections
        cls.node_attributes = import_node_attributes('NodeAttributes.xlsx')
        cls.node_connections = import_node_connections('NodeConnections.xlsx')

    def test_initialization(self):
        """Simulate running test"""
        sim = Simulation(red_team_params, blue_team_params, self.node_attributes, self.node_connections)
        victor = sim.start()
        self.assertEqual(victor, 'red')
            

if __name__ == "__main__":
    unittest.main()