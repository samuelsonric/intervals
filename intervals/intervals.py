from intervals.simple_function import Terms
from itertools import cycle, chain, islice
from collections import deque
from math import inf
from numpy import array, float64

class Intervals(Terms):
    def __init__(self, parity, endpoints):
        self.parity = bool(parity)
        self.endpoints = array(endpoints, float64)

    @classmethod
    def from_terms(cls, terms):
        coef, ep = zip(*terms)
        return cls(coef[0], ep)

    @classmethod
    def from_endpoints(cls, endpoints):
        ep = deque(endpoints) or deque((-inf,))
        if not (p := (-inf == ep[0])):
            ep.appendleft(-inf)
        if ep[-1] == inf:
            ep.pop()
        return cls(p, ep)
 
    @classmethod
    def from_pairs(cls, pairs):
        return cls.from_endpoints(chain.from_iterable(pairs))

    def iter_terms(self):
        p = self.parity
        yield from zip(cycle((p, not p)), self.endpoints)

    def iter_pairs(self):
        def filt(x):
            return x[0]
        def mapper(x):
            return x[1:]
        yield from map(mapper, filter(filt, self.iter_triples()))

    def __invert__(self):
        return type(self)(not self.parity, self.endpoints)

    def __sub__(self, other):
        return self & ~other

    def __xor__(self, other):
        return (self & ~other) | (other & ~self)

    def __eq__(self, other):
        return self.parity == other.parity and all(self.endpoints == other.endpoints)

    def __repr__(self):
        n = 6
        return f"{type(self).__name__}({', '.join(map(str, islice(self.iter_pairs(), n)))})"
