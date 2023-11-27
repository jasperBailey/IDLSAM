import unittest
from scheduler.models.onefactoriser import OneFactoriser


class TestOneFactoriser(unittest.TestCase):
    def setUp(self):
        self.onefact = OneFactoriser(8)
        self.onefact.oneFactorisations()

    @unittest.skip
    def testCreateEdges(self):
        print(f"edges: {self.onefact.getEdges()}")

    @unittest.skip
    def testInitialSol(self):
        print(self.onefact.getInitialSol())

    @unittest.skip
    def testGetOneFactors(self):
        print(len(self.onefact.getAllOneFactors()))

    # @unittest.skip
    def testGetOneFactorisations(self):
        print(len(self.onefact.getOneFactorisations()))

    @unittest.skip
    def testGetW1(self):
        for thingy in self.onefact.getW1():
            print(thingy)

    @unittest.skip
    def testGetOneFactorisationsAsLists(self):
        print(len(self.onefact.getOneFactorisationsAsLists()))

    @unittest.skip
    def testOnefactorisationUniqueness(self):
        for oneFactorisation in self.onefact.getOneFactorisations():
            count = 0
            for oneFactorisation2 in self.onefact.getOneFactorisations():
                if oneFactorisation == oneFactorisation2:
                    count += 1
            self.assertEqual(count, 1)

    @unittest.skip
    def testGetSchedules(self):
        self.assertEqual(31449600, len(self.onefact.getSchedules()))
