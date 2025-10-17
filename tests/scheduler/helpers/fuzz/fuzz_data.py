import random


def random_csv_data(n: int, bye=False, bias=0) -> list[str]:
    assert n > 1, "n must be greater than 1"
    assert not n % 2, "n must be multiple of 2 (for now)"

    data = []

    for i in range(n):
        line = f"Team{i}"
        for d in random.choices(
            (
                ",0",
                ",1",
                ",2",
                ",3",
                ",4",
                ",5",
                ",10",
                ",11",
                ",12",
                ",13",
                ",14",
                ",20",
                ",21",
                ",22",
                ",23",
                ",30",
                ",31",
                ",32",
                ",40",
                ",41",
                ",50",
            ),
            (10, 5, 4, 2, 1, 1, 6, 4, 2, 1, 1, 4, 2, 1, 1, 3, 2, 1, 2, 1, 1),
            k=7 * (n - 1),
        ):
            line += d
        data.append(line)

    return data
