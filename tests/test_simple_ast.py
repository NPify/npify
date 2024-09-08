from npify import Or


def test_or():
    Or.from_iter(i for i in range(5) if i != 2)
