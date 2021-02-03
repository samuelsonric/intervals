from intervals.simple_function import IterSimpleFunctionAlgebra, SimpleFunction
from operator import not_
from itertools import cycle, chain, islice, zip_longest
from collections import deque, OrderedDict
from math import inf

def terms_of_endpoints(endpoints, ll, ul):
    i = next(endpoints, None)
    if i is None:
        yield (0, ll)
        yield (1, ul)
    else:
        if ll < i:
            yield (0, ll)
        yield (1, i)
        yield from zip(cycle((0, 1)), endpoints)

class Intervals(SimpleFunction):
    def __init__(self, parity, endpoints):
        self.parity = bool(parity)
        self.endpoints = tuple(endpoints)
        self.alg = IterSimpleFunctionAlgebra()

    @classmethod
    def from_terms(cls, terms):
        coef, ep = zip(*terms)
        # coef, ep = zip(*self.alg.pwun(lambda x: bool(x), terms))
        return cls(coef[0], ep)

    @classmethod
    def from_endpoints(cls, endpoints, ll, ul):
        ep = deque(endpoints) or deque([ll, ul])
        if not (p := (ll == ep[0])):
            ep.appendleft(ll)
        return cls(p, ep)
            
    @classmethod
    def from_pairs(cls, pairs, ll, ul):
        return cls.from_endpoints(chain.from_iterable(pairs), ll, ul)

    def iter_terms(self):
        yield from zip(cycle((self.parity, not self.parity)), self.endpoints)

    def iter_pairs(self):
        def f(x):
            return x[0]
        def m(x):
            return x[1:]
        yield from map(m, filter(f, self.alg.triples(self.iter_terms())))

        #ep = islice(self.endpoints, not self.parity, None)
        #yield from zip_longest(ep, ep, fillvalue = inf)

    def compl(self):
        return self.from_terms(self.alg.pwun(not_, self.iter_terms()))

    def __and__(self, other):
        return self.min(other)

    def __or__(self, other):
        return self.max(other)

    def __eq__(self, other):
        return self.parity == other.parity and self.endpoints == other.endpoints

    def __repr__(self):
        n = 6
        return f"{type(self).__name__}({', '.join(map(str, islice(self.iter_pairs(), n)))})"
        
def composition_maps(coef, endpoints):
    cf = OrderedDict()
    fmap = []
    imap = []
    for n, p in enumerate(coef):
        if p in cf:
            i = cf[p]
        else:
            cf[p] = i = len(cf)
            imap.append([])
        fmap.append(i)
        imap[i] += endpoints[n:n+2]
    return (tuple(endpoints), tuple(cf), tuple(fmap), tuple(Intervals.from_endpoints(i, endpoints[0], inf) for i in imap))
        

