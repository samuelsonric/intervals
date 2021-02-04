from intervals.simple_function import SimpleFunction
from intervals.iterable import leb, pointwise_binary
from intervals.composition import Composition
from numpy import fromiter, array, float64
from functools import cached_property
from operator import mul


class SignedMeasure(SimpleFunction):
    def __matmul__(self, x):
        return leb(pointwise_binary(mul, self.iter_terms(), x.iter_terms()))


def push_forward(measure, imap):
    return fromiter(map(measure.__matmul__, imap), dtype=float64)


def joint(measure, ximap, yimap):
    def mapper(i):
        return push_forward(measure, map(i.__and__, yimap))

    return array(tuple(map(mapper, ximap)), dtype=float64)


def conditional_kernel(measure, ximap, yimap):
    j = joint(measure, ximap, yimap)
    s = j.sum(1)
    s = s + (s == 0)
    return (j.T / s).T


class PushForward:
    def __init__(self, measure, X):
        self.measure = measure
        self.X = X

    @cached_property
    def push_forward(self):
        return push_forward(self.measure, self.X.imap)

    def __matmul__(self, x):
        return self.push_forward @ x.coef


class ConditionalExpectation:
    def __init__(self, measure, X, Y):
        self.measure = measure
        self.X = X
        self.Y = Y

    @cached_property
    def kernel(self):
        return conditional_kernel(self.measure, self.X.imap, self.Y.imap)

    def __matmul__(self, x):
        coef = self.kernel @ x.coef
        return Composition.from_coef(self.X, coef)
