from intervals.terms import IterTerms
from intervals.simple_function import SimpleFunction
from numpy import unique, array, fromiter, maximum, minimum, float64
from collections import OrderedDict
from bisect import bisect_left

class CompositeFunction(IterTerms):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, x):
        return self.left[self.right(x)]

    @classmethod
    def from_array(cls, left, right):
        return cls(array(left, dtype=float64), right)

    @classmethod
    def from_simple_function(cls, sfun):
        left = OrderedDict()
        right = []
        for i in sfun.mat:
            right.append((left.setdefault(i[0], len(left)), i[1]))
        return cls.from_array(tuple(left), SimpleFunction.from_array(right))

    def iter_terms(self):
        for i in self.right.iter_terms():
            yield (self.left[int(i[0])], i[1])

    def __neg__(self):
        return type(self)(-self.left, self.right)

    def __add__(self, other):
        return type(self)(self.left + other.left, self.right)

    def __sub__(self, other):
        return type(self)(self.left - other.left, self.right)

    def __mul__(self, other):
        return type(self)(self.left * other.left, self.right)

    def __or__(self, other):
        return type(self)(maximum(self.left, other.left), self.right)

    def __and__(self, other):
        return type(self)(minimum(self.left, other.left), self.right)

    def __eq__(self, other):
        return all(self.left == other.left)

    def __le__(self, other):
        return all(self.left <= other.left)

    def __lt__(self, other):
        return all(self.left < other.left)
