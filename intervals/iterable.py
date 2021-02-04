from math import inf
from itertools import zip_longest
from numpy import linspace

def eq(x, y):
    return all(i == j for i, j in zip_longest(x, y))

def triples(x):
    i = next(x)
    for j in x:
        yield (*i, (i := j)[1])
    yield (*i, inf)

def leb_of_triple(i):
    return i[0] and i[0]*(i[2]-i[1])

def leb(x):
    return sum(map(leb_of_triple, triples(x)))

def reduce_terms(x):
    p = None
    for i in x:
        if not p == i[0]:
            p = i[0]
            yield i

def pointwise_binary(op, x, y):
    yield from reduce_terms(pointwise_binary_0(op, x, y))

def pointwise_unary(op, x):
    yield from reduce_terms(pointwise_unary_0(op, x))

def approx(fun, start, stop, num_steps):
    yield from reduce_terms(approx_0(fun, start, stop, num_steps))

def pointwise_binary_0(op, x, y):
    i = next(x)
    j = next(y)
    sentinel = (0, inf)

    while not i == j == sentinel:
        if i[1] < j[1]:
            yield (op(i[0], jh[0]), i[1])
            ih = i
            i = next(x, sentinel)
        elif j[1] < i[1]:
            yield (op(ih[0], j[0]), j[1])
            jh = j
            j = next(y, sentinel)
        else:
            yield (op(i[0], j[0]), i[1])
            ih = i
            jh = j
            i = next(x, sentinel)
            j = next(y, sentinel)

def pointwise_unary_0(op, x):
    for i in x:
        yield (op(i[0]), i[1])

def graph_of_fun(fun):
    return lambda x: (fun(x), x)

def approx_0(fun, start, stop, num_steps):
    yield (0, -inf)
    yield from map(graph_of_fun(fun), linspace(start, stop, num_steps, endpoint=False))
    yield (0, stop)
