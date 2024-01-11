from models.onefactoriser import OneFactoriser
from itertools import permutations
from models.pairing import Pairing


class TournamentScheduler:
    def __init__(self, teamsAvailabilities: dict):
        self.library = {}
        self.teams = list(teamsAvailabilities)
        self.teamsAvailabilities = [teamsAvailabilities[name] for name in self.teams]
        self._numTeams = len(list(self.teamsAvailabilities))
        self._numWeeks = self._numTeams - 1
        self._pairingsPerWeek = self._numTeams // 2

        self.minSolScore = self.calcMinSolScore()
        self.bestSol = None
        self.bestSolScore = 10000
        self.onefactoriser = OneFactoriser(self._numTeams)
        self._rangeNumWeeks = range(self._numWeeks)
        self.pairings = self.createPairings()
        self.oneFactorScores = self.calcOneFactorScores()

    def getOneFactorScores(self):
        return dict(self.oneFactorScores)

    def getBestSol(self):
        return self.bestSol

    def setBestSol(self, value):
        self.bestSol = value

    def getBestSolScore(self):
        return self.bestSolScore

    def setBestSolScore(self, value):
        self.bestSolScore = value

    def getTeamsAvailabilities(self) -> list:
        return self.teamsAvailabilities

    def getTeams(self):
        return self.teams

    def calcOneFactorScores(self):
        oneFactorMap = {}
        for oneFactor in self.onefactoriser.getAllOneFactors():
            weekScores = []
            for i in self._rangeNumWeeks:
                weekScores.append(0)
            for match in oneFactor:
                tMatch = tuple(match)
                for i in self._rangeNumWeeks:
                    weekScores[i] += self.pairings[tMatch[0]][
                        tMatch[1]
                    ].getWeekScores()[i]
            oneFactorMap[oneFactor] = weekScores
        return oneFactorMap

    def calcBestSchedule(self):
        bye = False
        if self.getTeams()[self._numTeams - 1] == "BYE":
            bye = True

        for onefactorisation in self.onefactoriser.oneFactorisations():
            for schedule in permutations(onefactorisation):
                score = 0
                for i in self._rangeNumWeeks:
                    for match in schedule[i]:
                        if not bye or (
                            match[0] != self._numTeams - 1
                            and match[1] != self._numTeams - 1
                        ):
                            score += self.pairings[match[0]][match[1]].getWeekScores()[
                                i
                            ]
                    if score >= self.bestSolScore:
                        break
                else:
                    self.setBestSolScore(score)
                    self.setBestSol(schedule)

        schedule = [tuple(week) for week in self.getBestSol()]
        teams = self.getTeams()

        weekDays = {
            0: "SUNDAY",
            1: "MONDAY",
            2: "TUESDAY",
            3: "WEDNESDAY",
            4: "THURSDAY",
            5: "FRIDAY",
            6: "SATURDAY",
        }

        toReturn = []
        for i in range(len(schedule)):
            toReturn.append([])
            for match in schedule[i]:
                toReturn[i].append(
                    [
                        teams[match[0]],
                        teams[match[1]],
                        weekDays[self.pairings[match[0]][match[1]].getBestDays()[i]],
                        self.pairings[match[0]][match[1]].getWeekScores()[i],
                    ]
                )

        return {
            "schedule": toReturn,
            "scheduleScore": self.getBestSolScore(),
            "teams": self.teams,
        }

    def createPairings(self) -> list:
        # Returns:
        #
        # list [frozenset, list] - a list where the first element of each entry is
        #   a frozenset containing the name of both teams involved in the pairing
        #   and the second element of each entry is a list of boolean values indicating
        #   whether that matchup can take place on that week

        teamsAvail = self.getTeamsAvailabilities()
        teamNames = self.getTeams()
        pairings = {}

        # create list of possible matchups and list of matchup availabilities
        # in each time period (week)
        for i in range(self._numTeams):
            pairings[i] = {}
            for j in range(i, self._numTeams):
                if i == j:
                    continue
                team1 = teamNames[i]
                team2 = teamNames[j]
                pairings[i][j] = Pairing.fromTeamAvailabilities(
                    team1, team2, teamsAvail[i], teamsAvail[j]
                )

        return pairings

    def calcMinSolScore(self):
        minScore = 0
        for team in self.getTeamsAvailabilities():
            for week in team:
                minScore += min(week)
        return minScore
