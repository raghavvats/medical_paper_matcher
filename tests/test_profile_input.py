import unittest
from unittest.mock import patch
from src.cli.profile_input import ProfileInputCLI
from src.models.profile import CustomerProfile

class TestProfileInputCLI(unittest.TestCase):
    def setUp(self):
        self.cli = ProfileInputCLI()

    @patch('builtins.input')
    def test_physical_characteristics_input(self, mock_input):
        # Mock user inputs for physical characteristics
        mock_input.side_effect = [
            "30",           # age
            "170.5",        # weight in lbs
            "70",           # height in inches
            "1"            # sex (1 for male)
        ]

        result = self.cli._get_physical_characteristics()
        
        self.assertEqual(result["age"], 30)
        self.assertEqual(result["weight"], 170.5)
        self.assertEqual(result["height"], 70)
        self.assertEqual(result["sex"], "male")

    @patch('builtins.input')
    def test_complete_profile_input(self, mock_input):
        # Mock all necessary inputs for a complete profile
        mock_input.side_effect = [
            # Physical characteristics
            "30", "170.5", "70", "1",  
            # Demographics
            "1",    # race
            "1",    # location
            # Medical history (empty lists for simplicity)
            "",     # preexisting conditions
            "",     # prior conditions
            "",     # surgeries
            "",     # medications
            # Lifestyle
            "1",    # athleticism
            "1",    # diet
            # Filename
            "test_profile"
        ]

        profile = self.cli.collect_profile()
        self.assertIsInstance(profile, CustomerProfile)

if __name__ == '__main__':
    unittest.main() 