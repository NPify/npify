from dataclasses import dataclass


class ListLike(list):
    def flatten(self):
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
    def __init__(*args):
        pass


class And(ListLike):
    def __init__(*args):
        pass


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

    def or_iter(self, iterator):
        print(" ".join(str(x.to_int(self.vars)) for x in iterator), file=self.file)

    def or_(self, *args):
        print(" ".join(str(x.to_int(self.vars)) for x in args), file=self.file)


def print_cnf(formula, file):
    printer = CNFPrinter(file)

    check_is_cnf(formula)

    for clause in formula:
        printer.or_iter(clause)


class NotCNFError(ValueError):
    pass


def check_is_cnf(formula):
    if not isinstance(formula, And):
        msg = "Root node is not a conjunction."
        raise NotCNFError(msg)

    for clause in formula:
        if not isinstance(clause, Or):
            msg = "Child node is not a disjunction."
            raise NotCNFError(msg)

        for literal in clause:
            if isinstance(literal, BooleanLiteral):
                continue
            if isinstance(literal, BooleanVariable):
                continue

            msg = (f"Expected a Boolean variable or a literal inside a clause, "
                   f"but found '{literal}'.")
            raise NotCNFError(msg)


class Visitor:
    def visit(self, obj):
        class_name = obj.__class__.__name__.lower()
        method = getattr(self, f"visit_{class_name}", None)
        if method:
            return method(obj)

        return self.default(obj)

    def default(self, obj):
        pass
