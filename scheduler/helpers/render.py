def render_match_line(i, j, week_idx, team_names, best_days, pairings, day_names):
    name1, name2 = team_names[i], team_names[j]

    if i == j:
        return f"  {name1} vs {name2} — Invalid matchup (same team)"

    if "BYE" in (name1, name2):
        return f"  {name1} vs {name2}"

    i_, j_ = max(i, j), min(i, j)
    try:
        best_day_index = best_days[i_][j_][week_idx]
        badness = pairings[i_][j_][week_idx]
        best_day_name = day_names[best_day_index]
        return f"  {name1} vs {name2} — Best day: {best_day_name}, Badness: {badness}"
    except IndexError:
        return f"  {name1} vs {name2} — Data missing for week {week_idx + 1}"


def render_human_schedule_with_badness(schedule, team_names, best_days, pairings):
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    output_lines = []

    for week_idx, week in enumerate(schedule):
        output_lines.append(f"Week {week_idx + 1}:")
        for i, j in week:
            line = render_match_line(
                i, j, week_idx, team_names, best_days, pairings, day_names
            )
            output_lines.append(line)
        output_lines.append("")

    return "\n".join(output_lines)
