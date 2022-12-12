from enum import Enum
from typing import Callable, Iterable, Literal, NamedTuple, TypeVar, overload

T = TypeVar("T")
U = TypeVar("U")

@overload
def nwise(iterable: Iterable[T], n: Literal[2]) -> Iterable[tuple[T, T]]: ...
@overload
def nwise(iterable: Iterable[T], n: Literal[3]) -> Iterable[tuple[T, T, T]]: ...
@overload
def nwise(iterable: Iterable[T], n: Literal[4]) -> Iterable[tuple[T, T, T, T]]: ...
@overload
def nwise(iterable: Iterable[T], n: Literal[5]) -> Iterable[tuple[T, T, T, T, T]]: ...
@overload
def nwise(
    iterable: Iterable[T], n: Literal[6]
) -> Iterable[tuple[T, T, T, T, T, T]]: ...
@overload
def nwise(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]: ...
@overload
def first(iterable: Iterable[T]) -> T: ...
@overload
def first(iterable: Iterable[T], default: U) -> T | U: ...
@overload
def grouped(iterable: Iterable[T], n: Literal[2]) -> Iterable[tuple[T, T]]: ...
@overload
def grouped(iterable: Iterable[T], n: Literal[3]) -> Iterable[tuple[T, T, T]]: ...
@overload
def grouped(iterable: Iterable[T], n: Literal[4]) -> Iterable[tuple[T, T, T, T]]: ...
@overload
def grouped(iterable: Iterable[T], n: Literal[5]) -> Iterable[tuple[T, T, T, T, T]]: ...
@overload
def grouped(
    iterable: Iterable[T], n: Literal[6]
) -> Iterable[tuple[T, T, T, T, T, T]]: ...
@overload
def grouped(iterable: Iterable[T], n: int) -> Iterable[tuple[T]]: ...
def flatten(iterable: Iterable[Iterable[T]]) -> Iterable[T]: ...

class Offset(NamedTuple):
    x: int
    y: int

class Direction(Enum):
    UP = Offset(0, -1)
    UP_LEFT = Offset(-1, -1)
    UP_RIGHT = Offset(1, -1)
    DOWN = Offset(0, 1)
    DOWN_LEFT = Offset(-1, 1)
    DOWN_RIGHT = Offset(1, 1)
    LEFT = Offset(-1, 0)
    RIGHT = Offset(0, 1)

CARDINAL_DIRECTIONS = (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)

def make_direction_range(
    height: int, width: int, *direction: Direction | Offset | tuple[int, int]
) -> Callable[[int, int], Iterable[tuple[int, int]]]: ...
def make_direction_ranges(
    height: int, width: int, *directions: Direction | Offset | tuple[int, int]
) -> tuple[Callable[[int, int], Iterable[tuple[int, int]]], ...]: ...
