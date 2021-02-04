from intervals.algebra import Poset
from intervals.iterable import (
    pointwise_binary,
    pointwise_unary,
    reduce_terms,
    triples,
    leb,
    eq,
)


class Terms(Poset):
    @classmethod
    def from_terms(cls, terms):
        ...

    def iter_terms(self):
        ...

    def iter_triples(self):
        yield from triples(self.iter_terms())

    def iter_nonzero_triples(self):
        filt = lambda x: x[0]
        yield from filter(filt, self.iter_triples())

    def pointwise_unary(self, op):
        return self.from_terms(pointwise_unary(op, self.iter_terms()))

    def pointwise_binary(self, op, other):
        return self.from_terms(
            pointwise_binary(op, self.iter_terms(), other.iter_terms())
        )

    def leb(self):
        return leb(self.iter_terms())

    def __call__(self, x):
        for i in self.iter_triples():
            if i[1] <= x < i[2]:
                return i[0]

    def __and__(self, other):
        return self.pointwise_binary(min, other)

    def __or__(self, other):
        return self.pointwise_binary(max, other)

    def __eq__(self, other):
        return eq(self.iter_terms(), other.iter_terms())

    def __le__(self, other):
        return self == self & other
