"""test for red_team"""
import unittest
from team import Team

class TestRedTeam(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, if any."""
        self.model_ID = "test_model"
        self.energy = 100
        self.potency = 80
        self.influence_factor = 1.5
        self.alignment = 50
        self.red_team_instance = Team(self.model_ID, self.energy, self.potency, self.influence_factor, self.alignment)

    def test_initialization(self):
        """Test the initialization of the red_team class."""
        self.assertEqual(self.red_team_instance._team, 'red')
        self.assertEqual(self.red_team_instance._energy, self.energy)
        self.assertEqual(self.red_team_instance._model_ID, self.model_ID)
        self.assertEqual(self.red_team_instance._potency, self.potency)
        self.assertEqual(self.red_team_instance._message_count, 0)
        self.assertEqual(self.red_team_instance._influence_factor, self.influence_factor)
        self.assertEqual(self.red_team_instance._alignment, self.alignment)

    def test_team(self):
        """Test the team method."""
        self.assertEqual(self.red_team_instance.team(), 'red')

    def test_next_round(self):
        """Test the next_round method."""
        self.red_team_instance.next_round()
        self.assertEqual(self.red_team_instance._message_count, 1)

        self.red_team_instance.next_round()
        self.assertEqual(self.red_team_instance._message_count, 2)

    def test_set_potency(self):
        """Test the set_potency method."""
        new_potency = 90
        self.red_team_instance.set_potency(new_potency)
        self.assertEqual(self.red_team_instance._potency, new_potency)
        
    def test_generate_message(self):
        """Test generating message"""
        message, potency = self.red_team_instance.generate_message()
        self.assertIsNotNone(message)
        self.assertIsNotNone(potency)
    
if __name__ == '__main__':
    unittest.main()
