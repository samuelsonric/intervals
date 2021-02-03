from intervals.simple_function import SimpleFunction

class SignedMeasure(SimpleFunction):
    def integrate(self, x):
        return self.alg.leb(self.alg.prod(self.iter_terms(), x.iter_terms()))

def push_forward(exp: SignedMeasure, imap):
    return tuple(map(exp.integrate, imap))

def joint(exp: SignedMeasure, ximap, yimap):
    def m(i):
        return push_forward(exp, map(lambda j: i&j, yimap))
    return tuple(map(m, ximap))
