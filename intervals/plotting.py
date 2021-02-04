from itertools import takewhile, dropwhile
import matplotlib.pyplot as plt


def get_bar_inputs(sfunc, start, stop):
    def mapper(i):
        return (i[0], i[1], i[2] - i[1])

    tfilt = lambda i: i[1] < stop
    dfilt = lambda i: i[2] < start

    g = map(mapper, takewhile(tfilt, dropwhile(dfilt, sfunc.iter_triples())))

    height, x, width = map(list, zip(*g))

    x[0] = start
    width[0] = width[1] - start
    width[-1] = stop - x[-1]

    return (x, height, width)


def plot_sfuncs(
    *sfuncs,
    xlim=(-10, 10),
    ylim=None,
    figsize=(8, 6),
    colors=("b", "g", "r", "c", "m", "y", "k"),
):
    plt.figure(figsize=figsize)
    for x, c in zip(sfuncs, cycle(colors)):
        plt.bar(*get_bar_inputs(x, *xlim), color=c)
    plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

    plt.show()
