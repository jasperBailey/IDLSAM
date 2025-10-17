import pytest
from scheduler.helpers.main import main


@pytest.mark.parametrize(
    "lines,bye,expect_bye_in_output",
    [
        (["A,1,2,3,4,5,6,7", "B,7,6,5,4,3,2,1"], False, False),
        (
            [
                "MOGGER,200,0,200,200,410,400,200,0,0,0,200,200,400,300,100,0,0,100,110,100,0,0,0,0,100,110,200,100,100,0,0,100,110,200,100",
                "CUSTARD,110,200,210,200,110,110,0,0,100,10,100,110,110,100,0,0,10,0,10,10,0,100,0,110,0,10,10,0,0,10,210,110,10,100,100",
                "PIZZA,50,260,160,220,550,550,460,0,210,120,220,50,100,100,0,210,120,220,250,0,0,0,210,120,220,150,100,0,0,210,120,220,150,0,0",
                "SABATA,210,110,200,210,400,300,310,100,0,200,10,110,10,100,0,0,100,100,110,100,100,0,0,200,10,200,100,100,0,0,100,100,200,0,100",
                "DEATH_ROE,15,20,200,110,110,110,10,10,120,100,100,150,110,110,10,20,10,60,160,10,110,10,20,10,20,160,10,10,10,20,10,20,160,110,110",
                "A_SQUIRREL,50,100,100,100,300,300,310,5,0,200,110,250,105,150,0,0,150,120,0,0,100,0,0,250,110,250,105,150,0,50,200,110,0,100,200",
            ],
            False,
            False,
        ),
    ],
)
def test_main_with_csv_lines_and_bye(lines, bye, expect_bye_in_output):
    schedule, badness, human_output = main(csv_lines=lines, bye=bye)
    print("Schedule:", schedule)
    print("Badness:", badness)
    print("Human Output:", human_output)
    assert schedule is not None
    assert isinstance(badness, (int, float))
    assert isinstance(human_output, str)
    assert "Week" in human_output
    if expect_bye_in_output:
        assert "BYE" in human_output
    else:
        assert "BYE" not in human_output


def test_main_with_csv_file_and_bye():
    schedule, badness, human_output = main(
        csv_path="C:/Users/jaspe/Documents/Work/IDLSAM/data/s39.csv", bye=True
    )
    print("Schedule:", schedule)
    print("Badness:", badness)
    print("Human Output:", human_output)
    assert schedule is not None
    assert isinstance(badness, (int, float))
    assert isinstance(human_output, str)
    assert "Week" in human_output
    assert "BYE" in human_output
