class Pairing:
    def __init__(
        self, team1Name: str, team2Name: str, weekScores: list, bestDays: list
    ) -> None:
        self.team1Name = team1Name
        self.team2Name = team2Name
        self.teams = frozenset([team1Name, team2Name])
        self.weekScores = weekScores
        self.bestDays = bestDays
        self.bestWeeks = list(range(len(weekScores)))
        self.bestWeeks.sort(key=lambda i: weekScores[i])

    def getTeams(self):
        return self.teams

    def getTeam1Name(self):
        return self.team1Name

    def getTeam2Name(self):
        return self.team2Name

    def getWeekScores(self):
        return self.weekScores

    def getBestDays(self):
        return self.bestDays

    def getBestWeeks(self):
        return self.bestWeeks

    @classmethod
    def fromTeamAvailabilities(
        cls, team1Name: str, team2Name: str, team1Avail: list, team2Avail: list
    ) -> list:
        numWeeks = len(team1Avail)
        weekScores = []
        bestDays = []
        for week in range(numWeeks):
            bestDayValue = 1000
            bestDay = 0

            for day in range(7):
                dayValue = team1Avail[week][day] + team2Avail[week][day]
                if dayValue < bestDayValue:
                    bestDayValue = dayValue
                    bestDay = day

            weekScores.append(bestDayValue)
            bestDays.append(bestDay)

        return cls(team1Name, team2Name, weekScores, bestDays)

    def __repr__(self) -> str:
        return f'Pairing("{self.getTeam1Name()}", "{self.getTeam2Name()}", {self.getWeekScores()}, {self.getBestDays()})'
