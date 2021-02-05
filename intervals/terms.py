from intervals.algebra import Poset
from intervals.iterable import (
    pointwise_binary,
    pointwise_unary,
    terms_of_triples,
    triples_of_terms,
    leb,
    eq,
    call,
)
from operator import mul, neg, add, sub


class IterTerms:
    repr_pat = "{}*({}, {})"
    repr_sep = " + "
    repr_num = 3

    def iter_terms(self):
        ...

    def iter_triples(self):
        yield from triples_of_terms(self.iter_terms())

    def leb(self):
        return leb(self.iter_terms())

    def __call__(self, x):
        call(x, self.iter_terms())

    def __eq__(self, other):
        return eq(self.iter_terms(), other.iter_terms())

    def __repr__(self):
        l = []
        for n, i in enumerate(self.iter_triples()):
            if n < self.repr_num:
                l.append(self.repr_pat.format(*i))
            else:
                l.append("...")
                break
        return f"{type(self).__name__}({self.repr_sep.join(l)})"


class IterTermsLattice(IterTerms, Poset):
    @classmethod
    def from_terms(cls, terms):
        raise NotImplementedError

    @classmethod
    def from_triples(cls, triples):
        return cls.from_terms(terms_of_triples(iter(triples)))

    def __and__(self, other):
        return self.from_terms(
            pointwise_binary(min, self.iter_terms(), other.iter_terms())
        )

    def __or__(self, other):
        return self.from_terms(
            pointwise_binary(max, self.iter_terms(), other.iter_terms())
        )

    def __mul__(self, other):
        return self.from_terms(
            pointwise_binary(mul, self.iter_terms(), other.iter_terms())
        )

    def __le__(self, other):
        return self == self & other


class IterTermsAlgebra(IterTermsLattice):
    def __neg__(self, other):
        return self.from_terms(pointwise_unary(neg, self.iter_terms()))

    def __add__(self, other):
        return self.from_terms(
            pointwise_binary(add, self.iter_terms(), other.iter_terms())
        )

    def __sub__(self, other):
        return self.from_terms(
            pointwise_binary(sub, self.iter_terms(), other.iter_terms())
        )
