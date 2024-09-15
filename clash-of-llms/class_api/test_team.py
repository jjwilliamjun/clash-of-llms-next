"""Tests for team"""
import unittest
from team import Team

class TestRedTeam(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, if any."""
        self.red_team_instance = Team("red", "test_model", 0, 0.7, 40, 60)
        self.blue_team_instance = Team("blue", "test_model", 500, 0.5, 40, 70)

    def test_initialization(self):
        """Test the initialization of the team classes."""
        self.assertEqual(self.red_team_instance._team, 'red')
        self.assertEqual(self.red_team_instance._model_ID, "test_model")
        self.assertEqual(self.red_team_instance._energy, 0)
        self.assertEqual(self.red_team_instance._message_count, 0)
        self.assertEqual(self.red_team_instance._max_cost, 40)
        self.assertEqual(self.red_team_instance._influence_factor, 0.7)
        self.assertEqual(self.red_team_instance._alignment, 60)
        
        self.assertEqual(self.blue_team_instance._team, 'blue')
        self.assertEqual(self.blue_team_instance._model_ID, "test_model")
        self.assertEqual(self.blue_team_instance._energy, 500)
        self.assertEqual(self.blue_team_instance._message_count, 0)
        self.assertEqual(self.blue_team_instance._max_cost, 40)
        self.assertEqual(self.blue_team_instance._influence_factor, 0.5)
        self.assertEqual(self.blue_team_instance._alignment, 70)

    def test_next_round(self):
        """Test the next_round method."""
        self.red_team_instance.next_round()
        self.assertEqual(self.red_team_instance._message_count, 1)

        self.red_team_instance.next_round()
        self.assertEqual(self.red_team_instance._message_count, 2)

    def test_set_potency(self):
        """Test update energy level"""
        self.blue_team_instance.update_energy_level(100)
        self.assertEqual(self.blue_team_instance._energy, 400)
        
        self.blue_team_instance.update_energy_level(600)
        self.assertEqual(self.blue_team_instance._energy, 0)
        
    def test_generate_message(self):
        """Test generating message"""
        self.red_team_instance.generate_message()
        self.assertIsNotNone(self.red_team_instance._message)
        self.assertIsNotNone(self.red_team_instance._potency)
        
    def test_energy_cost(self):
        """Test the calculation of energy cost"""
        self.red_team_instance.generate_message()
        self.assertIsNotNone(self.red_team_instance._potency)
        self.assertIsNotNone(self.red_team_instance._max_cost)
        self.assertEqual(self.red_team_instance.energy_cost(), self.red_team_instance._max_cost * (self.red_team_instance._potency / 100))
    
if __name__ == '__main__':
    unittest.main()
