from collections import namedtuple
from enum import Enum
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
    iterator = iter(iterable)
    if default is _SENTINEL:
        return next(iterator)

    return next(iterator, default)


def grouped(iterable, n):
    return zip(*[iter(iterable)] * n)


def flatten(iterable):
    return chain.from_iterable(iterable)


Offset = namedtuple("Offset", ["x", "y"])


class Direction(Enum):
    UP_LEFT = Offset(-1, -1)
    UP = Offset(0, -1)
    UP_RIGHT = Offset(1, -1)
    LEFT = Offset(-1, 0)
    RIGHT = Offset(1, 0)
    DOWN_LEFT = Offset(-1, 1)
    DOWN = Offset(0, 1)
    DOWN_RIGHT = Offset(1, 1)


CARDINAL_DIRECTIONS = (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)


def make_direction_range(height, width, offset):
    def dir_range(x, y):
        x += x_offset
        y += y_offset
        while 0 <= x < width and 0 <= y < height:
            yield x, y
            x += x_offset
            y += y_offset

    x_offset, y_offset = offset.value if isinstance(offset, Direction) else offset
    return dir_range


def make_direction_ranges(height, width, *directions):
    return tuple(make_direction_range(height, width, offset) for offset in directions)
