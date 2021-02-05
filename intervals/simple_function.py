from intervals.terms import IterTermsAlgebra
from intervals.iterable import approx
from numpy import array, float64
from itertools import islice
from bisect import bisect

class SimpleFunction(IterTermsAlgebra):
    def __init__(self, mat):
        self.mat = mat

    def __call__(self, x):
        return self.mat[bisect(self.mat[:, 1], x) - 1, 0]

    @classmethod
    def from_array(cls, arr):
        return cls(array(arr, dtype=float64))

    @classmethod
    def from_terms(cls, terms):
        return cls.from_array(tuple(terms))

    @classmethod
    def from_function(cls, fun, start=-10, stop=10, num_steps=10):
        return cls.from_terms(approx(fun, start, stop, num_steps))

    @classmethod
    def from_intervals(cls, intervals):
        return cls.from_terms(intervals.iter_terms())

    @classmethod
    def from_composite_function(cls, cfun):
        return cls.from_terms(cfun.iter_terms())

    def iter_terms(self):
        yield from map(tuple, self.mat)

    def __neg__(self):
        return type(self)(self.mat * (-1, 0))

