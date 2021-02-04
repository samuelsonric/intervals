from intervals.terms import IntegrableFunction
from intervals.simple_function import SimpleFunction
from intervals.algebra import Poset
from numpy import unique, array, fromiter, maximum, minimum, float64


class Composition(IntegrableFunction, Poset):
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

    def to_simple_function(self):
        return SimpleFunction(fromiter(map(self.coef.__getitem__, self.fmap), dtype=float64), self.endpoints)

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
        if isinstance(other, type(self)) and self.sfunc is other.sfunc:
            return self.from_coef(self.sfunc, self.coef + other.coef)
        return self.to_simple_function() + other

    def __sub__(self, other):
        if isinstance(other, type(self)) and self.sfunc is other.sfunc:
            return self.from_coef(self.sfunc, self.coef - other.coef)
        return self.to_simple_function() - other

    def __mul__(self, other):
        if isinstance(other, type(self)) and self.sfunc is other.sfunc:
            return self.from_coef(self.sfunc, self.coef * other.coef)
        return self.to_simple_function() * other

    def __or__(self, other):
        if isinstance(other, type(self)) and self.sfunc is other.sfunc:
            return self.from_coef(self.sfunc, maximum(self.coef, other.coef))
        return self.to_simple_function() * other

    def __and__(self, other):
        if isinstance(other, type(self)) and self.sfunc is other.sfunc:
            return self.from_coef(self.sfunc, minimum(self.coef, other.coef))
        return self.to_simple_function() & other

    def __le__(self, other):
        return self == self & other

    def __repr__(self):
        return f'{type(self).__name__}({repr(self.coef)})'
