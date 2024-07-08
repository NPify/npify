from dataclasses import dataclass
from itertools import chain
from io import StringIO

from timeit import timeit

def bool_var(cls):
    cls = dataclass(frozen=True, slots=True)(cls)
    return cls


class Expression():
    pass

class BooleanVariable():
    def __invert__(self):
        return BooleanLiteral(self, negated=True)

    def to_int(self, varDict):
        return varDict[self]



@dataclass(slots=True)
class BooleanLiteral():
    variable: BooleanVariable
    negated: bool = False
    
    def __str__(self):
        if self.negated:
            return f'~{self.variable}'
        else:
            return str(self.variable)

    def __invert__(self):
        return BooleanLiteral(self.variable, negated=not self.negated)

    def to_int(self, varDict):
        if self.negated:
            return -varDict[self.variable]
        else:
            return varDict[self.variable]



@bool_var
class Match(BooleanVariable):
    pigeon: int
    hole: int

    def __str__(self):
        return f'x{self.pigeon, self.hole}'


class VarDict(dict):
    def __init__(self):
        self.num_vars = 0

    def __missing__(self, key):
        self.num_vars += 1
        return self.num_vars

class CNFPrinter:
    def __init__(self, file):
        self.file = file
        self.vars = VarDict()

    def or_iter(self, iterator):
        print(' '.join(str(x.to_int(self.vars)) for x in iterator), file=self.file)

    def or_(self, *args):
        print(' '.join(str(x.to_int(self.vars)) for x in args), file=self.file)


def php_nice(n):
    npigeons = n
    nholes = n
    pigeons = list(range(npigeons))
    holes = list(range(nholes))

    buffer = StringIO()
    encoder = CNFPrinter(buffer)

    for p in pigeons:
        encoder.or_iter(Match(p, h) for h in holes)

    for h in holes:
        for p1 in pigeons:
            for p2 in pigeons:
                if p1 != p2:
                    encoder.or_(~Match(p1, h), ~Match(p2, h))

    return buffer.getvalue()


def php_raw(n):
    npigeons = n
    nholes = n
    pigeons = list(range(npigeons))
    holes = list(range(nholes))

    variables = VarDict()


    buffer = StringIO() 


    for p in pigeons:
        print(*(variables[p, h] for h in holes), file = buffer)

    for h in holes:
        for p1 in pigeons:
            for p2 in pigeons:
                if p1 != p2:
                    print(-variables[p1,h], -variables[p2,h], file = buffer)

    return buffer.getvalue()

class Builder:
    """ Build an abstract syntax tree that can later be evaluated. """

    def forall(self, **kwargs):
        for key, value in kwargs:
            ...

        return self

    def if_(self, **kwargs):
        for key, value in kwargs:
            ...

        return self

    def or_(self, *args):
        for value in args:
            ...

        return self


def generate(ast: Builder, file: StringIO):
    """ Evaluate the given abstract syntax tree and write thre result to the given file. """
    ...

def php_builder():
    builder = Builder()

    one_hole_per_pigeon = builder.forall(p=pigeons).or_iter(var("Match(p,h)"), h=holes)
    one_pigeon_per_hole = builder.forall(h=holes).forall(p1=pigeons).forall(p2=pigeons).if_(p1__neq='p2').or_('~Match(p1,h)', '~Match(p2, h)')


    buffer = StringIO()
    generate(Builder().and_(one_hole_per_pigeon, one_pigeon_per_hole), buffer)
    return buffer.getvalue()

    # builder.forall(p=pigeons).at_least_one(var('Match(p,h)').for_(h=holes))



def main():
    print('nice', timeit('php_nice(40)', number=10, globals=globals()))
    print('raw', timeit('php_raw(40)', number=10, globals=globals()))
    print('builder', timeit('php_builder(40)', number=10, globals=globals()))

    a = php_nice(40)
    b = php_raw(40)
    c = php_builder(40)

    assert a == b
    assert b == c




if __name__ == '__main__':
    main()
