from intervals.algebra import IterAlgebra, Poset
from intervals.iterable import iter_pwbin, iter_pwun
from math import inf

class IterSimpleFunctionAlgebra(IterAlgebra):
    def pwbin(self, op, x, y):
        yield from iter_pwbin(op, x, y)

    def pwun(self, op, x):
        yield from iter_pwun(op, x)

    def leb(self, x):
        s = 0
        i = next(x)
        for j in x:
            s += i[0]*(j[1]-i[1])
            i = j
        if i[0]:
            s += i[0]*inf
        return s

class SimpleFunction(Poset):
    def __init__(self, terms):
        self.terms = tuple(terms)
        self.alg = IterSimpleFunctionAlgebra()

    @classmethod
    def from_terms(cls, terms):
        return cls(terms)

    def iter_terms(self):
        yield from self.terms

    def __neg__(self):
        return self.from_terms(self.alg.neg(self.iter_terms()))

    def __mul__(self, other):
        return self.from_terms(self.alg.prod(self.iter_terms(), other.iter_terms()))

    def __add__(self, other):
        return self.from_terms(self.alg.sum(self.iter_terms(), other.iter_terms()))

    def __sub__(self, other):
        return self.from_terms(self.alg.diff(self.iter_terms(), other.iter_terms()))

    def max(self, other):
        return self.from_terms(self.alg.max(self.iter_terms(), other.iter_terms()))

    def min(self, other):
        return self.from_terms(self.alg.min(self.iter_terms(), other.iter_terms()))

    def smul(self, a):
        return self.from_terms(self.alg.smul(a, self.iter_terms()))

    def pwbin(self, op, other):
        return self.from_terms(self.alg.pwbin(op, self.iter_terms(), other.iter_terms()))

    def pwun(self, op):
        return self.from_terms(self.alg.pwun(op, self.iter_terms()))

    def leb(self):
        return self.alg.leb(self.iter_terms())

    def __eq__(self, other):
        return self.terms == other.terms

    def __le__(self, other):
        return self == self.min(other)
