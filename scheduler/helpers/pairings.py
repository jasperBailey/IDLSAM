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
    WEEKS = N - 1
    assert TOTAL_DAYS >= WEEKS * 7, f"data doesn't extend to the full {WEEKS} weeks"

    pairings = [[[] for _ in range(N)] for _ in range(N)]
    best_days = [[[] for _ in range(N)] for _ in range(N)]

    # Create the individual team game cost matrix indexed by week rather than day
    team_costs_by_week = []
    for i in range(N):
        team_costs_by_week.append([])
        for w in range(WEEKS):
            team_costs_by_week[i].append(float("inf"))
            for d in range(7):
                day_idx = w * 7 + d
                badness = team_costs[i][day_idx]
                if badness < team_costs_by_week[i][w]:
                    team_costs_by_week[i][w] = badness

    # Create the pairing cost matrix
    for i in range(N):
        for j in range(i):
            for w in range(WEEKS):
                min_badness = float("inf")
                best_day = -1
                for d in range(7):
                    day_idx = w * 7 + d
                    badness = team_costs[i][day_idx] + team_costs[j][day_idx]
                    if badness < min_badness:
                        min_badness = badness
                        best_day = d
                pairings[i][j].append(min_badness)
                best_days[i][j].append(best_day)

    # Create the matrix of the additional cost of having a pairing on a certain week,
    # relative to the lower bound case
    pairing_differentials = []
    for teamA in range(len(pairings)):
        pairing_differentials.append([])
        for teamB in range(teamA):
            pairing_differentials[teamA].append([])
            pairing = pairings[teamA][teamB]
            for week in range(len(pairings) - 1):
                pairing_differentials[teamA][teamB].append(pairing[week])
                pairing_differentials[teamA][teamB][week] -= team_costs_by_week[teamA][
                    week
                ]
                pairing_differentials[teamA][teamB][week] -= team_costs_by_week[teamB][
                    week
                ]

    return pairings, pairing_differentials, best_days, team_names
