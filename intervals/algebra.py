class Poset:
    def __eq__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        return self <= other and not self == other
