from intervals.terms import IntegrableFunctionLattice
from intervals.intervals import Intervals
from intervals.iterable import approx
from intervals.constants import MAX_REPR
from numpy import unique, fromiter, array, float64
from operator import mul, add, sub
from functools import cached_property
from itertools import islice, cycle


class SimpleFunction(IntegrableFunctionLattice):
    def __init__(self, coef, endpoints):
        self.coef = array(coef, dtype=float64)
        self.endpoints = array(endpoints, dtype=float64)

    @classmethod
    def from_terms(cls, terms):
        return cls(*zip(*terms))

    @classmethod
    def approx(cls, fun, start, stop, num_steps):
        return cls.from_terms(approx(fun, start, stop, num_steps))

    @classmethod
    def indicator(cls, intervals):
        p = intervals.parity
        return cls(
            fromiter(
                islice(cycle((p, not p)), len(intervals.endpoints)), dtype=float64
            ),
            intervals.endpoints,
        )

    def iter_terms(self):
        yield from zip(self.coef, self.endpoints)

    @cached_property
    def ccoef_fmap(self):
        return unique(self.coef, return_inverse=True)

    @property
    def fmap(self):
        return self.ccoef_fmap[1]

    @property
    def ccoef(self):
        return self.ccoef_fmap[0]

    @cached_property
    def imap(self):
        imap = {}
        for i in self.iter_triples():
            imap.setdefault(i[0], []).append(i[1:])
        return tuple(map(Intervals.from_pairs, map(imap.__getitem__, self.ccoef)))

    @property
    def coef(self):
        return self._coef

    @coef.setter
    def coef(self, value):
        self._coef = value
        if hasattr(self, "ccoef_fmap"):
            del self.ccoef_fmap
        if hasattr(self, "imap"):
            del self.imap

    def __neg__(self):
        return type(self)(-self.coef, self.endpoints)

    def __mul__(self, other):
        return self.pointwise_binary(mul, other)

    def __add__(self, other):
        return self.pointwise_binary(add, other)

    def __sub__(self, other):
        return self.pointwise_binary(sub, other)

    def __repr__(self):
        def to_str(i):
            return "{}*({}, {})".format(*i)

        l = list(map(to_str, islice(self.iter_nonzero_triples(), MAX_REPR + 1)))
        if len(l) == MAX_REPR + 1:
            l[-1] = "..."
        return f"{type(self).__name__}({' + '.join(l)})"
