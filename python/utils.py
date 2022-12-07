from itertools import chain, pairwise, tee

_SENTINEL = object()


def nwise(iterable, n):
    if n <= 1:
        raise ValueError(f"expected n higher than one, got {n}")

    elif n == 2:
        return pairwise(iterable)

    iterators = tee(iterable, n)
    for shift, iterator in enumerate(iterators):
        for _ in range(shift):
            next(iterator, None)

    return zip(*iterators)


def first(iterable, default=_SENTINEL):
    if default is _SENTINEL:
        return next(iter(iterable))

    return next(iter(iterable), default)


def grouped(iterable, n):
    return zip(*[iter(iterable)] * n)


def flatten(iterable):
    return chain.from_iterable(iterable)
