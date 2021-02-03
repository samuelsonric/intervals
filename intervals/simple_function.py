from intervals.algebra import IterAlgebra, Poset
from intervals.iterable import iter_pwbin, iter_pwun, reduce_terms
from math import inf
from itertools import islice

class IterSimpleFunctionAlgebra(IterAlgebra):
    def pwbin(self, op, x, y):
        yield from iter_pwbin(op, x, y)

    def pwun(self, op, x):
        yield from iter_pwun(op, x)

    def triples(self, x):
        i = next(x)
        for j in x:
            yield (*i, (i := j)[1])
        yield (*i, inf)

    def leb(self, x):
        def m(i):
            return i[0] and i[0]*(i[2]-i[1])
        return sum(map(m, self.triples(x)))

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
        return self.alg.eq(self.iter_terms(), other.iter_terms()) 

    def __le__(self, other):
        return self == self.min(other)

    def __repr__(self):
        n = 6
        return f"{type(self).__name__}({', '.join(map(str, islice(self.alg.triples(self.iter_terms()), n)))})"

def iter_approx(f, ll, ul, n):
    for i in range(n):
        x = ll + (ul-ll)*(i/n)
        yield(f(x), x)
    yield (0, ul)

def approx(f, ll, ul, n):
    return SimpleFunction.from_terms(iter_approx(f, ll, ul, n))
