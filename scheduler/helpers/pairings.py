def compute_pairings_from_schedule_lines(lines):
    team_costs = []
    team_names = []

    for line in lines:
        parts = line.strip().split(",")
        team_names.append(parts[0])
        costs = list(map(int, parts[1:]))
        team_costs.append(costs)

    N = len(team_costs)
    TOTAL_DAYS = len(team_costs[0])
    ROUNDS = N - 1
    assert TOTAL_DAYS >= 7 + (
        ROUNDS * 7
    ), f"data doesn't extend to the full {ROUNDS} rounds"

    pairings = [[[] for _ in range(N)] for _ in range(N)]
    best_days = [[[] for _ in range(N)] for _ in range(N)]

    # Create the individual team game cost matrix indexed by round rather than day
    team_costs_by_round = []
    for i in range(N):
        team_costs_by_round.append([])

        team_costs_by_round[i].append(float("inf"))
        for d in range(14):
            badness = team_costs[i][d]
            if badness < team_costs_by_round[i][0]:
                team_costs_by_round[i][0] = badness

        for r in range(1, ROUNDS):
            team_costs_by_round[i].append(float("inf"))
            for d in range(7):
                day_idx = r * 7 + d
                badness = team_costs[i][day_idx]
                if badness < team_costs_by_round[i][r]:
                    team_costs_by_round[i][r] = badness

    # Create the pairing cost matrix
    for i in range(N):
        for j in range(i):
            min_badness = float("inf")
            best_day = -1
            for d in range(14):
                badness = team_costs[i][d] + team_costs[j][d]
                if badness < min_badness:
                    min_badness = badness
                    best_day = d
            pairings[i][j].append(min_badness)
            best_days[i][j].append(best_day)

            for r in range(1, ROUNDS):
                min_badness = float("inf")
                best_day = -1
                for d in range(7):
                    day_idx = r * 7 + d
                    badness = team_costs[i][day_idx] + team_costs[j][day_idx]
                    if badness < min_badness:
                        min_badness = badness
                        best_day = d
                pairings[i][j].append(min_badness)
                best_days[i][j].append(best_day)

    # Create the matrix of the additional cost of having a pairing on a certain round,
    # relative to the lower bound case
    pairing_differentials = []
    for teamA in range(len(pairings)):
        pairing_differentials.append([])
        for teamB in range(teamA):
            pairing_differentials[teamA].append([])
            pairing = pairings[teamA][teamB]
            for round in range(len(pairings) - 1):
                pairing_differentials[teamA][teamB].append(pairing[round])
                pairing_differentials[teamA][teamB][round] -= team_costs_by_round[
                    teamA
                ][round]
                pairing_differentials[teamA][teamB][round] -= team_costs_by_round[
                    teamB
                ][round]

    return pairings, pairing_differentials, best_days, team_names
