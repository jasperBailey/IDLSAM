from ortools.sat.python import cp_model


def solve_schedule(pairings4teams, bye=False):
    N = len(pairings4teams)
    WEEKS = N - 1
    model = cp_model.CpModel()

    match = {}
    for i in range(N):
        for j in range(i + 1, N):
            for w in range(WEEKS):
                match[(i, j, w)] = model.NewBoolVar(f"match_{i}_{j}_week{w}")

    # Each pair plays once
    for i in range(N):
        for j in range(i + 1, N):
            model.AddExactlyOne(match[(i, j, w)] for w in range(WEEKS))

    # Team plays at most once per week
    for t in range(N):
        for w in range(WEEKS):
            weekly_matches = []
            for o in range(N):
                if t < o:
                    weekly_matches.append(match[(t, o, w)])
                elif o < t:
                    weekly_matches.append(match[(o, t, w)])
            model.AddAtMostOne(weekly_matches)

    # Objective: minimize total badness, ignore matches involving the ghost BYE team
    total_badness = []
    for i in range(N):
        for j in range(i + 1, N):
            for w in range(WEEKS):
                if bye and (i == N - 1 or j == N - 1):
                    continue
                cost = pairings4teams[max(i, j)][min(i, j)][w]
                total_badness.append(match[(i, j, w)] * cost)

    model.Minimize(sum(total_badness))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule = [[] for _ in range(WEEKS)]
        for i in range(N):
            for j in range(i + 1, N):
                for w in range(WEEKS):
                    if solver.Value(match[(i, j, w)]) == 1:
                        schedule[w].append((i, j))
        return schedule, solver.ObjectiveValue()
    else:
        return None, None
