from dataclasses import dataclass


class ListLike(list):
    def __init__(self, *args):
        self.extend(args)

    def flatten(self):
        # TODO: flatten recursively
        cls = self.__class__
        result = cls()

        for child in self:
            if isinstance(child, cls):
                result.extend(child.flatten())
            else:
                result.append(child)

        return result

    @classmethod
    def from_iter(cls, iterable):
        result = cls()
        result.extend(iterable)
        return result


class Or(ListLike):
    pass


class And(ListLike):
    pass


class AtMostLiterals(ListLike):
    pass


@dataclass
class AtMost:
    literals: AtMostLiterals
    bound: int


def at_most_one(literals):
    return AtMost(literals, 1)


def bool_var(cls):
    # return dataclass(frozen=True, slots=True)(cls)
    return cls


class Expression:
    pass


class BooleanVariable:
    def __invert__(self):
        return BooleanLiteral(self, negated=True)

    def to_int(self, var_dict):
        return var_dict[self]


@dataclass(slots=True)
class BooleanLiteral:
    variable: BooleanVariable
    negated: bool = False

    def __str__(self):
        if self.negated:
            return f"~{self.variable}"

        return str(self.variable)

    def __invert__(self):
        return BooleanLiteral(self.variable, negated=not self.negated)

    def to_int(self, var_dict):
        if self.negated:
            return -var_dict[self.variable]

        return var_dict[self.variable]


class VarDict(dict):
    def __init__(self):
        self.num_vars = 0

    def __missing__(self, key):
        self.num_vars += 1
        self[key] = self.num_vars
        return self.num_vars


class CNFPrinter:
    def __init__(self, file):
        self.file = file
        self.vars = VarDict()

    def append(self, clause):
        clause = to_cnf(clause)
        print(" ".join(str(x.to_int(self.vars)) for x in clause), file=self.file)

    def extend(self, clauses):
        for clause in clauses:
            self.append(clause)


def print_cnf(formula, file):
    printer = CNFPrinter(file)

    check_is_cnf(formula)

    for clause in formula:
        printer.append(clause)


class NotCNFError(ValueError):
    pass


class NotAClauseError(ValueError):
    pass


def check_is_cnf(formula):
    if not isinstance(formula, And):
        msg = (f"Expected conjunction (And) at root node, but found"
               f"'{type(formula).__name__}'.")
        raise NotCNFError(msg)

    for clause in formula:
        if not isinstance(clause, Or):
            msg = ("Expected a disjunction (Or) at child node, but found."
                   f"'{type(clause).__name__}'.")
            raise NotCNFError(msg)

        try:
            check_is_clause(clause)
        except NotAClauseError as e:
            raise NotCNFError from e


def check_is_clause(clause):
    for literal in clause:
        if isinstance(literal, BooleanLiteral):
            continue
        if isinstance(literal, BooleanVariable):
            continue

        msg = (f"Expected a Boolean variable or a literal inside a clause, "
               f"but found '{type(literal).__name__}'.")
        raise NotCNFError(msg)


def to_cnf(formula):
    if isinstance(formula, AtMost):
        if formula.bound != 1:
            raise NotImplementedError

        for literal in formula.literals:
            if (not isinstance(literal, BooleanVariable) and
                    not isinstance(literal, BooleanLiteral)):
                raise NotImplementedError

        result = And()
        for var1 in formula.literals:
            for var2 in formula.literals:
                if var1 != var2:
                    result.append(Or(~var1, ~var2))

        return result
    if isinstance(formula, Or):
        try:
            check_is_clause(formula)
        except NotAClauseError as e:
            raise NotImplementedError from e

        return formula

    raise NotImplementedError


class Visitor:
    def visit(self, obj):
        class_name = obj.__class__.__name__.lower()
        method = getattr(self, f"visit_{class_name}", None)
        if method:
            return method(obj)

        return self.default(obj)

    def default(self, obj):
        pass
