from intervals.terms import IterTermsLattice
from itertools import cycle, chain, islice, zip_longest
from bisect import bisect
from math import inf
from numpy import array, float64
from collections import deque


class Intervals(IterTermsLattice):
    repr_pat = "({1}, {2})"
    repr_sep = ", "

    def __init__(self, parity, endpoints):
        self.parity = bool(parity)
        self.endpoints = array(endpoints, float64)

    def __call__(self, x):
        return self.parity == bisect(self.endpoints, x) % 2

    @classmethod
    def from_terms(cls, terms):
        coef, ep = zip(*terms)
        return cls(coef[0], ep)

    @classmethod
    def from_endpoints(cls, endpoints):
        ep = deque(endpoints)
        if not (p := (ep and -inf == ep[0])):
            ep.appendleft(-inf)
        return cls(p, ep)

    @classmethod
    def from_pairs(cls, pairs):
        return cls.from_endpoints(chain.from_iterable(pairs))

    def iter_terms(self):
        c = cycle((self.parity, not self.parity))
        yield from zip(c, self.endpoints)

    def iter_pairs(self):
        ep = islice(self.endpoints, not self.parity, None)
        yield from zip_longest(ep, ep, fillvalue=inf)

    def __invert__(self):
        return type(self)(not self.parity, self.endpoints)

    def __sub__(self, other):
        return self & ~other

    def __xor__(self, other):
        return (self & ~other) | (other & ~self)

    def __eq__(self, other):
        return self.parity == other.parity and all(self.endpoints == other.endpoints)
