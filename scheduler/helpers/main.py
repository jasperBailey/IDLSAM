from .pairings import compute_pairings_from_schedule_lines
from .solver import solve_schedule
from .render import render_human_schedule_with_badness


def main(csv_lines=None, csv_path=None, bye=True):
    """
    Main entry point for scheduling.
    Provide either csv_lines (list of CSV strings) or csv_path (path to CSV file).
    Returns: (schedule, badness, human_readable_output)
    """
    if csv_lines is None and csv_path is not None:
        with open(csv_path) as f:
            csv_lines = f.readlines()
    elif csv_lines is None:
        raise ValueError("Either csv_lines or csv_path must be provided.")

    pairings, pairing_differentials, best_days, team_names = (
        compute_pairings_from_schedule_lines(csv_lines)
    )
    bye = "BYE" in team_names
    schedule, badness = solve_schedule(pairing_differentials, bye)
    human_output = render_human_schedule_with_badness(
        schedule, team_names, best_days, pairings
    )
    return schedule, badness, human_output


if __name__ == "__main__":
    # Example usage: run only when executed directly
    schedule, badness, human_output = main(csv_path="./data/AD_B.csv", bye=True)
    print("Best schedule:", schedule)
    print("Total badness:", badness)
    print(human_output)
