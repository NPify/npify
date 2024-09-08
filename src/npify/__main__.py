from io import StringIO
from timeit import timeit

from npify import VarDict


def php_raw(n):
    npigeons = n
    nholes = n
    pigeons = list(range(npigeons))
    holes = list(range(nholes))

    variables = VarDict()

    buffer = StringIO()

    for p in pigeons:
        print(*(variables[p, h] for h in holes), file=buffer)

    for h in holes:
        for p1 in pigeons:
            for p2 in pigeons:
                if p1 != p2:
                    print(-variables[p1, h], -variables[p2, h], file=buffer)

    return buffer.getvalue()


class Builder:
    """Build an abstract syntax tree that can later be evaluated."""

    def forall(self, **_kwargs):
        # for key, value in kwargs:
        #     ...

        return self

    def if_(self, **_kwargs):
        # for key, value in kwargs:
        #     ...

        return self

    def or_(self, *_args):
        # for value in args:
        #     ...

        return self

    def and_(self, *_args):
        # for value in args:
        #     ...

        return self


def generate(_ast: Builder, _file: StringIO):
    """
    Evaluate the given abstract syntax tree and write thre result to the
    given file.
    """


def var(_name):
    pass


def php_builder(n):
    npigeons = n
    nholes = n
    pigeons = list(range(npigeons))
    holes = list(range(nholes))

    builder = Builder()

    one_hole_per_pigeon = builder.forall(p=pigeons).or_iter(var("Match(p,h)"), h=holes)
    one_pigeon_per_hole = (
        builder.forall(h=holes)
        .forall(p1=pigeons)
        .forall(p2=pigeons)
        .if_(p1__neq="p2")
        .or_("~Match(p1,h)", "~Match(p2, h)")
    )

    buffer = StringIO()
    generate(Builder().and_(one_hole_per_pigeon, one_pigeon_per_hole), buffer)
    return buffer.getvalue()

    # builder.forall(p=pigeons).at_least_one(var('Match(p,h)').for_(h=holes))


def main():
    print("nice", timeit("php_nice(40)", number=10, globals=globals()))  # noqa T203
    print("raw", timeit("php_raw(40)", number=10, globals=globals()))  # noqa T203
    # print('builder', timeit('php_builder(40)', number=10, globals=globals()))


if __name__ == "__main__":
    main()
