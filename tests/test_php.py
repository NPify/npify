from dataclasses import dataclass
from io import StringIO

import pytest

import npify
from npify import And, BooleanVariable, CNFPrinter, Or


@npify.bool_var
@dataclass(frozen=True, slots=True)
class Match(BooleanVariable):
    pigeon: int
    hole: int

    def __str__(self):
        return f"x{self.pigeon, self.hole}"


Match(1, 2)


@pytest.mark.parametrize(("npigeons", "nholes"), [(4, 4)])
def test_php_explicit(npigeons, nholes):
    pigeons = list(range(npigeons))
    holes = list(range(nholes))

    buffer = StringIO()

    formula = And()

    for p in pigeons:
        formula.append(Or.from_iter(Match(p, h) for h in holes))

    for h in holes:
        for p1 in pigeons:
            for p2 in pigeons:
                if p1 != p2:
                    formula.append(Or(~Match(p1, h), ~Match(p2, h)))

    npify.print_cnf(formula, buffer)

    print(buffer.getvalue())


@pytest.mark.parametrize(("npigeons", "nholes"), [(4, 4)])
def test_php_atmost(npigeons, nholes):
    pigeons = list(range(npigeons))
    holes = list(range(nholes))

    buffer = StringIO()
    printer = CNFPrinter(buffer)

    for p in pigeons:
        printer.append(Or.from_iter(Match(p, h) for h in holes))

    for h in holes:
        constraint = npify.at_most_one(Match(p, h) for h in holes)
        printer.append(constraint)

    assert len(printer.vars) == npigeons * nholes
    print(buffer.getvalue())
