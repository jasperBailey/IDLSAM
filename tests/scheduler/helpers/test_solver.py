import pytest
from scheduler.helpers.pairings import compute_pairings_from_schedule_lines
from scheduler.helpers.solver import solve_schedule


@pytest.mark.parametrize(
    "lines",
    [
        (["A,1,1,1,1,1,1,1", "B,2,2,2,2,2,2,2"]),
    ],
)
def test_solve_schedule_basic(lines):
    pairings, pairing_differentials, best_days, team_names = (
        compute_pairings_from_schedule_lines(lines)
    )
    schedule, badness = solve_schedule(pairing_differentials, bye=False)
    assert schedule is not None
    assert isinstance(badness, (int, float))
