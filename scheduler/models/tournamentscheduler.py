from models.onefactoriser import OneFactoriser
from itertools import permutations
from models.pairing import Pairing
import asyncio
import aiohttp
import time


class TournamentScheduler:
    def __init__(self, teamsAvailabilities: dict):
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
        self.subschedules = dict()

    def getSubschedules(self):
        return self.subschedules

    def setSubschedules(self, subschedules):
        self.subschedules = subschedules

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

    def getAllWeekScores(self):
        allWeekScores = {}
        for i in self.pairings:
            allWeekScores[i] = {}
            for j in self.pairings[i]:
                allWeekScores[i][j] = self.pairings[i][j].getWeekScores()
        return allWeekScores

    def gatherAllSubSols(self):
        start_time = time.time()

        async def main():
            async with aiohttp.ClientSession() as session:
                bye = False
                if self.getTeams()[self._numTeams - 1] == "BYE":
                    bye = True
                tasks = []
                for onefactorisation in self.onefactoriser.oneFactorisations():
                    onefactorisationToSend = []
                    for onefactor in onefactorisation:
                        onefactorisationToSend.append(tuple(onefactor))
                    url = "https://21p2ys0os2.execute-api.eu-north-1.amazonaws.com/Prod/subschedule/"
                    tasks.append(
                        asyncio.ensure_future(
                            self.getSubschedule(
                                session, url, onefactorisationToSend, bye
                            )
                        )
                    )

                subschedules = await asyncio.gather(*tasks)
                self.setSubschedules(subschedules)

        asyncio.run(main())
        print(
            "--- %s seconds to gather all subschedules---" % (time.time() - start_time)
        )

    async def getSubschedule(self, session, url, onefactorisation, bye):
        json = {
            "oneFactorisation": onefactorisation,
            "pairingScores": self.getAllWeekScores(),
            "bye": bye,
        }
        async with session.post(url, json=json) as resp:  ###
            subschedule = await resp.json()
            return subschedule["subschedule"]

    def calcBestSchedule(self):
        for solution in self.getSubschedules():
            if solution["scheduleScore"] < self.getBestSolScore():
                self.setBestSolScore(solution["scheduleScore"])
                self.setBestSol(solution["schedule"])

        return self.getFormattedBestSchedule()

    def getFormattedBestSchedule(self):
        schedule = self.getBestSol()
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

        return {"schedule": toReturn, "scheduleScore": self.getBestSolScore()}

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
