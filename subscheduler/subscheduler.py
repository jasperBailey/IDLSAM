from itertools import permutations


class SubScheduler:
    def __init__(self, oneFactorisation: list, pairingScores: dict, bye: bool):
        self.bye = bye
        self.onefactorisation = oneFactorisation
        self.pairingScores = pairingScores

        self._numTeams = len(pairingScores)
        self._numWeeks = self._numTeams - 1

        self.bestSol = None
        self.bestSolScore = 10000
        self._rangeNumWeeks = range(self._numWeeks)

    def getOneFactorisation(self):
        return self.oneFactorisation[:]

    def getBestSol(self):
        return self.bestSol

    def setBestSol(self, value):
        self.bestSol = value

    def getBestSolScore(self):
        return self.bestSolScore

    def setBestSolScore(self, value):
        self.bestSolScore = value

    def calcBestSchedule(self):
        for schedule in permutations(self.getOneFactorisation()):
            score = 0
            for i in self._rangeNumWeeks:
                for match in schedule[i]:
                    if not self.bye or (
                        match[0] != self._numWeeks and match[1] != self._numWeeks
                    ):
                        score += self.pairingScores[match[0]][match[1]][i]
                if score >= self.bestSolScore:
                    break
            else:
                self.setBestSolScore(score)
                self.setBestSol(schedule)

        return {
            "schedule": [tuple(week) for week in self.getBestSol()],
            "scheduleScore": self.getBestSolScore(),
        }
