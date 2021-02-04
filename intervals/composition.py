from intervals.terms import IntegrableFunction
from numpy import unique, array, fromiter, maximum, minimum, float64


class Composition(IntegrableFunction):
    def __init__(self, sfunc, coef):
        self.sfunc = sfunc
        self.coef = array(coef, dtype=float64)

    @classmethod
    def from_coef(cls, sfunc, coef):
        return cls(sfunc, coef)

    @classmethod
    def from_callable(cls, sfunc, fun=lambda x: x):
        return cls.from_coef(sfunc, fromiter(map(fun, sfunc.ccoef), float64))

    def iter_terms(self):
        yield from zip(map(self.coef.__getitem__, self.fmap), self.endpoints)

    @property
    def endpoints(self):
        return self.sfunc.endpoints

    @property
    def fmap(self):
        return self.sfunc.fmap

    @property
    def imap(self):
        return self.sfunc.imap

    def __neg__(self):
        return self.from_coef(self.sfunc, -self.coef)

    def __add__(self, other):
        return self.from_coef(self.sfunc, self.coef + other.coef)

    def __sub__(self, other):
        return self.from_coef(self.sfunc, self.coef - other.coef)

    def __mul__(self, other):
        return self.from_coef(self.sfunc, self.coef * other.coef)

    def __or__(self, other):
        return self.from_coef(self.sfunc, maximum(self.coef, other.coef))

    def __and__(self, other):
        return self.from_coef(self.sfunc, minimum(self.coef, other.coef))

    def __eq__(self, other):
        return self.coef == other.coef

    def __le__(self, other):
        return all(self.coef <= other.coef)

    def __lt__(self, other):
        return all(self.coef < other.coef)
