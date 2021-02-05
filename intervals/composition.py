from intervals.terms import IntegrableFunction
from intervals.simple_function import SimpleFunction
from numpy import unique, array, fromiter, maximum, minimum, float64

class Composition(IntegrableFunction):
    def __init__(self, sfun, coef):
        self.sfun = sfun
        self.coef = array(coef, float64)

    @classmethod
    def from_sfun(cls, sfun):
        return cls(sfun, sfun.ccoef)

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
        return all(self.coef == other.coef)

    def __le__(self, other):
        return all(self.coef <= other.coef)

    def __lt__(self, other):
        return all(self.coef < other.coef)

    def __repr__(self):
        return f'{type(self).__name__}({repr(self.coef)})'
