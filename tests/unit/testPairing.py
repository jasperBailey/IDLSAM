import unittest
import json
from models.pairing import *


class TestPairing(unittest.TestCase):
    def setUp(self):
        with open("data/datainv.json") as f:
            data = json.load(f)
        keys = list(data["teamAvailabilities"].keys())
        team1 = keys[0]
        team2 = keys[1]
        team1Avail = data["teamAvailabilities"][team1]
        team2Avail = data["teamAvailabilities"][team2]
        self.pairing = Pairing.fromTeamAvailabilities(
            team1, team2, team1Avail, team2Avail
        )

    @unittest.skip
    def testCalcBestDays(self):
        self.assertEqual([3, 3, 3, 3, 0, 3, 3], self.pairing.getBestDays())
        self.assertEqual([0, 0, 0, 0, 100, 100, 0], self.pairing.getWeekScores())
