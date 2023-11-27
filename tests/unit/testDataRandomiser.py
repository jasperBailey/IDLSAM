import unittest
from data.datarandomiser import *


class TestRandomiser(unittest.TestCase):
    def setUp(self):
        self.numTeams = 8
        self.randomiser = DataRandomiser(self.numTeams)

    @unittest.skip
    def testGenData(self):
        print(self.randomiser.randomData())
