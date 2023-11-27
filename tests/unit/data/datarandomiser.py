import random


class DataRandomiser:
    def __init__(self, numTeams, availScore=0, maybeScore=1, cantScore=10):
        self.numTeams = numTeams
        self.nextData = (availScore, maybeScore, cantScore)

    def randomData(self):
        result = {"teamAvailabilities": {}}
        for i in range(self.numTeams):
            teamData = []

            for j in range(self.numTeams - 1):
                weekData = []
                for k in range(7):
                    dayScore = 0
                    for l in range(5):
                        dayScore += random.choices(
                            self.nextData, weights=(12, 1, 2), k=1
                        )[0]
                    weekData.append(dayScore)
                teamData.append(weekData[:])
            result["teamAvailabilities"][f"team{i}"] = teamData[:]

        return result
