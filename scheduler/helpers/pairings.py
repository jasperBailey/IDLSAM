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
    assert TOTAL_DAYS % 7 == 0, "Each team must have full weeks (multiples of 7 days)"
    WEEKS = TOTAL_DAYS // 7

    pairings = [[[] for _ in range(N)] for _ in range(N)]
    best_days = [[[] for _ in range(N)] for _ in range(N)]

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

    return pairings, best_days, team_names
