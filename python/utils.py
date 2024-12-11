from __future__ import annotations

import math
from enum import Enum
from functools import cached_property
from itertools import chain
from itertools import pairwise
from itertools import tee

_SENTINEL = object()


def nwise(iterable, n):
    if n == 2:
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


class Vector:
    __slots__ = ("_values",)

    def __init__(self, x=0, y=0, /):
        if isinstance(x, tuple):
            if len(x) != 2:
                raise ValueError("Vector init length is expected to be 2")

            x, y = x

        self._values = (x, y)

    @property
    def x(self, /):
        return self._values[0]

    @property
    def y(self, /):
        return self._values[1]

    @cached_property
    def length(self, /):
        return math.hypot(*self)

    def normalize(self, /):
        return self.__class__(self.x / self.length, self.y / self.length)

    def __neg__(self, /):
        return self.__class__(-self.x, -self.y)

    def __mul__(self, other, /):
        if not isinstance(other, int | float):
            return NotImplemented

        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self, other, /):
        return self.__mul__(other)

    def __truediv__(self, other, /):
        if not isinstance(other, int | float):
            return NotImplemented

        return self.__class__(self.x / other, self.y / other)

    def __floordiv__(self, other, /):
        if not isinstance(other, int | float):
            return NotImplemented

        return self.__class__(self.x // other, self.y // other)

    def __add__(self, other, /):
        if isinstance(other, Vector):
            return self.__class__(self.x + other.x, self.y + other.y)

        if isinstance(other, int | float):
            return self.__class__(self.x + other, self.y + other)

        return NotImplemented

    def __radd__(self, other, /):
        return self.__add__(other)

    def __sub__(self, other, /):
        if isinstance(other, Vector):
            return self.__class__(self.x - other.x, self.y - other.y)

        if isinstance(other, int | float):
            return self.__class__(self.x - other, self.y - other)

        return NotImplemented

    def __rsub__(self, other, /):
        return self.__sub__(other)

    def __lt__(self, other, /):
        if isinstance(other, int | float):
            return self.x < other > self.y

        if isinstance(other, Vector):
            return self.x < other.x and self.y < other.y

        if isinstance(other, tuple):
            if len(other) != 2:
                return NotImplemented
            return self.x < other[0] and self.y < other[1]

        return NotImplemented

    def __le__(self, other, /):
        if isinstance(other, int | float):
            return self.x <= other >= self.y

        if isinstance(other, Vector):
            return self.x <= other.x and self.y <= other.y

        if isinstance(other, tuple):
            if len(other) != 2:
                return NotImplemented
            return self.x <= other[0] and self.y <= other[1]

        return NotImplemented

    def __eq__(self, other, /):
        if isinstance(other, int | float):
            return self.x == other == self.y

        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y

        if isinstance(other, tuple):
            if len(other) != 2:
                return False
            return self.x == other[0] and self.y == other[1]

        return False

    def __ne__(self, other, /):
        if isinstance(other, int | float):
            return self.x != other != self.y

        if isinstance(other, Vector):
            return self.x != other.x and self.y != other.y

        if isinstance(other, tuple):
            if len(other) != 2:
                return False
            return self.x != other[0] and self.y != other[1]

        return False

    def __ge__(self, other, /):
        if isinstance(other, int | float):
            return self.x >= other <= self.y

        if isinstance(other, Vector):
            return self.x >= other.x and self.y >= other.y

        if isinstance(other, tuple):
            if len(other) != 2:
                return NotImplemented
            return self.x >= other[0] and self.y >= other[1]

        return NotImplemented

    def __gt__(self, other, /):
        if isinstance(other, int | float):
            return self.x > other < self.y

        if isinstance(other, Vector):
            return self.x > other.x and self.y > other.y

        if isinstance(other, tuple):
            if len(other) != 2:
                return NotImplemented
            return self.x > other[0] and self.y > other[1]

        return NotImplemented

    def __str__(self, /):
        return f"<{self.x}|{self.y}>"

    def __iter__(self, /):
        return iter(self._values)

    def __repr__(self, /):
        return f"{type(self).__name__}(x={self.x}, y={self.y})"

    def __hash__(self, /):
        return self._values.__hash__()


class VectorF(Vector):
    def __str__(self, /):
        return f"<{self.x:f}|{self.y:f}>"

    def __repr__(self, /):
        return f"{type(self).__name__}(x={self.x:f}, y={self.y:f})"


class Direction(Enum):
    UP_LEFT = Vector(-1, -1)
    UP = Vector(0, -1)
    UP_RIGHT = Vector(1, -1)
    LEFT = Vector(-1, 0)
    RIGHT = Vector(1, 0)
    DOWN_LEFT = Vector(-1, 1)
    DOWN = Vector(0, 1)
    DOWN_RIGHT = Vector(1, 1)


CARDINAL_DIRECTIONS = (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)


def range2d(width, height):
    for y in range(height):
        for x in range(width):
            yield x, y


def make_direction_range(height, width, offset):
    def dir_range(position):
        position += offset
        while (0, 0) <= position < (width, height):
            yield position
            position += offset

    if isinstance(offset, Direction):
        offset = offset.value
    elif isinstance(offset, tuple):
        offset = Vector(*offset)

    return dir_range


def make_direction_ranges(height, width, *directions):
    return tuple(make_direction_range(height, width, offset) for offset in directions)


LETTER_LOOKUP = {
    0x699F99: "A",
    0xE9E99E: "B",
    0x698896: "C",
    0xF8E888: "F",
    0x698B97: "G",
    0x9ACAA9: "K",
    0x88888F: "L",
    0xE99E88: "P",
    0xE99EA9: "R",
    0x999996: "U",
    0xF1248F: "Z",
}

LETTER_WIDTH = 4
LETTER_HEIGHT = 6
LETTER_COUNT = 8


def convert_letters(board):
    char_codes = [0] * LETTER_COUNT

    iterator = iter(board)
    for _ in range(LETTER_HEIGHT):
        for index in range(LETTER_COUNT):
            for _ in range(LETTER_WIDTH):
                char_codes[index] <<= 1
                if next(iterator):
                    char_codes[index] |= 1
            # Skip one char of padding
            next(iterator)

    return "".join(LETTER_LOOKUP.get(char_code, f"(0x{char_code:X})") for char_code in char_codes)
