from operator import add, mul

class Poset:
    def __eq__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        return other <= self

    def __lt__(self, other):
        return self <= other and not self == other

    def gt(self, other):
        return self >= other and not self == other

class IterGroup:
    def neg(self, x):
        raise NotImplementedError

    def sum(self, x, y):
        raise NotImplementedError

    def diff(self, x, y):
        yield from self.sum(x, self.neg(y))

    def eq(self, x, y):
        return all(i == j for i, j in zip(x, y))

class IterVectorSpace(IterGroup):
    def neg(self, x):
        yield from self.smul(-1, x)

    # scalar multiplication
    def smul(self, a, x):
        raise NotImplementedError

class IterAlgebra(IterVectorSpace):
    def abs(self, x):
        yield from self.pwun(abs, x)

    # positive part
    def pprt(self, x):
        yield from self.pwun(lambda x: x*(x>0), x)

    # negative part
    def nprt(self, x):
        yield from self.neg(self.pprt(self.neg(x)))

    # pointwise evaluation of unary operation
    def pwun(self, op, x):
        raise NotImplementedError

    def smul(self, a, x):
        yield from self.pwun(lambda x: a*x, x)

    # pointwise evaluation of binary operation
    def pwbin(self, op, x, y):
        raise NotImplementedError

    def max(self, x, y):
        yield from self.pwbin(max, x, y)

    def min(self, x, y):
        yield from self.pwbin(min, x, y)

    def prod(self, x, y):
        yield from self.pwbin(mul, x, y)

    def sum(self, x, y):
        yield from self.pwbin(add, x, y)
