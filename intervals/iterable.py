from math import inf

def iter_pwbin(op, x, y):
    yield from reduce_terms(pwbin(op, x, y))

def iter_pwun(op, x):
    yield from reduce_terms(pwun(op, x))

def reduce_terms(terms):
    p = None
    for i in terms:
        if not p == i[0]:
            p = i[0]
            yield i

def pwbin(op, x, y):
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

def pwun(op, x):
    for i in x:
        yield (op(i[0]), i[1])
