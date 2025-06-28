import pytest
from scheduler.helpers.pairings import compute_pairings_from_schedule_lines


@pytest.mark.parametrize(
    "lines,expected_team_names",
    [
        (["TeamA,1,2,3,4,5,6,7", "TeamB,7,6,5,4,3,2,1"], ["TeamA", "TeamB"]),
    ],
)
def test_compute_pairings_from_schedule_lines_basic(lines, expected_team_names):
    pairings, best_days, team_names = compute_pairings_from_schedule_lines(lines)
    assert team_names == expected_team_names
    assert len(pairings) == 2
    assert len(pairings[1][0]) == 1  # 1 week
    assert best_days[1][0][0] in range(7)
