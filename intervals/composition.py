from intervals.iterable import leb
from numpy import unique, array, fromiter, maximum, minimum, float64

class Composition:
    def __init__(self, sfunc, coef):
        self.sfunc = sfunc
        self.coef = array(coef, dtype=float64)

    @classmethod
    def from_coef(cls, sfunc, coef):
        return cls(sfunc, coef)

    @classmethod
    def from_callable(cls, sfunc, fun=lambda x: x):
        return cls.from_coef(sfunc, fromiter(map(fun, sfunc.get_ccoef()), float))

    def iter_terms(self):
        yield from zip(map(self.coef.__getitem__, self.get_fmap()), self.get_endpoints())

    def get_endpoints(self):
        return self.sfunc.endpoints

    def get_fmap(self):
        return self.sfunc.get_fmap()

    def get_ccoef(self):
        return self.sfunc.get_ccoef()

    def get_imap(self):
        return self.sfunc.get_imap()

    def leb(self):
        return leb(self.iter_terms())

    def __neg__(self):
        return self.from_coef(self.sfunc, -self.coef)

    def __add__(self, other):
        return self.from_coef(self.sfunc, self.coef + other.coef)

    def __sub__(self, other):
        return self.from_coef(self.sfunc, self.coef - other.coef)

    def __mul__(self, other):
        return self.from_coef(self.sfunc, self.coef * other.coef)

    def __or__(self, other):
        return self.from_coef(self.sfunc, maximum(self.coef, other.coef))

    def __and__(self, other):
        return self.from_coef(self.sfunc, minimum(self.coef, other.coef))

    def __eq__(self, other):
        return self.coef == other.coef

    def __le__(self, other):
        return all(self.coef <= other.coef)

    def __lt__(self, other):
        return all(self.coef < other.coef)
