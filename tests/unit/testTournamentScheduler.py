import unittest
import json
from models.tournamentscheduler import *
from data.datarandomiser import *


class TestScheduler(unittest.TestCase):
    def setUp(self):
        with open("data/datainv.json") as f:
            self.data = json.load(f)
        self.numTeams = len(self.data["teamAvailabilities"])
        self.scheduler = TournamentScheduler(self.data["teamAvailabilities"])

    @unittest.skip
    def testBruteForce(self):
        [result, score] = self.scheduler.getBestSchedule(
            curSolution=self.scheduler.emptySolution()
        )
        print(result)
        self.assertEqual(score, 400)

    @unittest.skip
    def testGetTeams(self):
        self.assertEqual(
            len(self.scheduler.getTeamsAvailabilities()),
            8,
        )
        print(self.scheduler.getTeamsAvailabilities())

    @unittest.skip
    def testGetBestSchedule(self):
        print(self.scheduler.calcBestSchedule())

    @unittest.skip
    def testGetOneFactorScores(self):
        print(self.scheduler.getOneFactorScores())

    @unittest.skip
    def testGetBestScheduleRandomData(self):
        randomiser = DataRandomiser(self.numTeams)
        minscores = []
        scores = []
        diffs = []
        for i in range(100):
            print(i)
            randScheduler = TournamentScheduler(
                randomiser.randomData()["teamAvailabilities"]
            )
            result = randScheduler.calcBestSchedule()
            print(result)
            scores.append(result[1])
            minscores.append(result[2])
            diffs.append(result[1] - result[2])

        print(f"scores: {scores}")
        print(f"minscores: {minscores}")
        print(f"diffs: {diffs}")
