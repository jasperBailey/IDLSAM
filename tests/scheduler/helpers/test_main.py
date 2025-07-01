import pytest
from scheduler.helpers.main import main


@pytest.mark.parametrize(
    "lines,bye,expect_bye_in_output",
    [
        (["A,1,2,3,4,5,6,7", "B,7,6,5,4,3,2,1"], False, False),
        (
            [
                "A,1,2,3,4,5,6,7,1,2,3,4,5,6,7,1,2,3,4,5,6,7",
                "B,7,6,5,4,3,2,1,1,2,3,4,5,6,7,1,2,3,4,5,6,7",
                "C,1,1,1,1,1,1,1,1,2,3,4,5,6,7,1,2,3,4,5,6,7",
                "BYE,0,0,0,0,0,0,0,1,2,3,4,5,6,7,1,2,3,4,5,6,7",
            ],
            True,
            True,
        ),
    ],
)
def test_main_with_csv_lines_and_bye(lines, bye, expect_bye_in_output):
    schedule, badness, human_output = main(csv_lines=lines, bye=bye)
    assert schedule is not None
    assert isinstance(badness, (int, float))
    assert isinstance(human_output, str)
    assert "Week" in human_output
    if expect_bye_in_output:
        assert "BYE" in human_output
    else:
        assert "BYE" not in human_output
