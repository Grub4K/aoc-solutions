from enum import Enum
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import Literal
from typing import TypeVar
from typing import overload

_T = TypeVar("_T")
_U = TypeVar("_U")

@overload
def nwise(iterable: Iterable[_T], n: Literal[1]) -> Iterable[tuple[_T]]: ...
@overload
def nwise(iterable: Iterable[_T], n: Literal[2]) -> Iterable[tuple[_T, _T]]: ...
@overload
def nwise(iterable: Iterable[_T], n: Literal[3]) -> Iterable[tuple[_T, _T, _T]]: ...
@overload
def nwise(iterable: Iterable[_T], n: Literal[4]) -> Iterable[tuple[_T, _T, _T, _T]]: ...
@overload
def nwise(iterable: Iterable[_T], n: Literal[5]) -> Iterable[tuple[_T, _T, _T, _T, _T]]: ...
@overload
def nwise(iterable: Iterable[_T], n: Literal[6]) -> Iterable[tuple[_T, _T, _T, _T, _T, _T]]: ...
@overload
def nwise(iterable: Iterable[_T], n: int) -> Iterable[tuple[_T, ...]]: ...
@overload
def first(iterable: Iterable[_T]) -> _T: ...
@overload
def first(iterable: Iterable[_T], default: _U) -> _T | _U: ...
@overload
def grouped(iterable: Iterable[_T], n: Literal[2]) -> Iterable[tuple[_T, _T]]: ...
@overload
def grouped(iterable: Iterable[_T], n: Literal[3]) -> Iterable[tuple[_T, _T, _T]]: ...
@overload
def grouped(iterable: Iterable[_T], n: Literal[4]) -> Iterable[tuple[_T, _T, _T, _T]]: ...
@overload
def grouped(iterable: Iterable[_T], n: Literal[5]) -> Iterable[tuple[_T, _T, _T, _T, _T]]: ...
@overload
def grouped(iterable: Iterable[_T], n: Literal[6]) -> Iterable[tuple[_T, _T, _T, _T, _T, _T]]: ...
@overload
def grouped(iterable: Iterable[_T], n: int) -> Iterable[tuple[_T, ...]]: ...
def flatten(iterable: Iterable[Iterable[_T]]) -> Iterable[_T]: ...

class Vector:
    @overload
    def __init__(self, x: int = 0, y: int = 0, /): ...
    @overload
    def __init__(self, x: tuple[int, int], /): ...
    @property
    def x(self, /) -> int: ...
    @property
    def y(self, /) -> int: ...
    @property
    def length(self, /) -> int: ...
    def normalize(self, /) -> Vector: ...
    def __neg__(self, /) -> Vector: ...
    def __mul__(self, other: int, /) -> Vector: ...
    def __rmul__(self, other: int, /) -> Vector: ...
    def __truediv__(self, other: int, /) -> Vector: ...
    def __floordiv__(self, other: int, /) -> Vector: ...
    def __add__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __radd__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __sub__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __rsub__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __lt__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __le__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __eq__(self, other: object, /) -> bool: ...
    def __ne__(self, other: object, /) -> bool: ...
    def __ge__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __gt__(self, other: int | Vector | tuple[int, int], /) -> Vector: ...
    def __iter__(self, /) -> Iterator[int]: ...
    def __hash__(self, /) -> int: ...

class VectorF:
    @overload
    def __init__(self, x: float = 0, y: float = 0, /): ...
    @overload
    def __init__(self, x: tuple[float, float], /): ...
    @property
    def x(self, /) -> float: ...
    @property
    def y(self, /) -> float: ...
    @property
    def length(self, /) -> float: ...
    def normalize(self, /) -> VectorF: ...
    def __neg__(self, /) -> VectorF: ...
    def __mul__(self, other: float, /) -> VectorF: ...
    def __rmul__(self, other: float, /) -> VectorF: ...
    def __truediv__(self, other: float, /) -> VectorF: ...
    def __floordiv__(self, other: float, /) -> VectorF: ...
    def __add__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __radd__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __sub__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __rsub__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __lt__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __le__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __eq__(self, other: object, /) -> bool: ...
    def __ne__(self, other: object, /) -> bool: ...
    def __ge__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __gt__(self, other: float | VectorF | tuple[float, float], /) -> VectorF: ...
    def __iter__(self, /) -> Iterator[float]: ...
    def __hash__(self, /) -> int: ...

class Direction(Enum):
    UP_LEFT = Vector(-1, -1)
    UP = Vector(0, -1)
    UP_RIGHT = Vector(1, -1)
    LEFT = Vector(-1, 0)
    RIGHT = Vector(1, 0)
    DOWN_LEFT = Vector(-1, 1)
    DOWN = Vector(0, 1)
    DOWN_RIGHT = Vector(1, 1)

CARDINAL_DIRECTIONS = ...

def range2d(width: int, height: int) -> Iterable[tuple[int, int]]: ...
def make_direction_range(
    height: int, width: int, *direction: Direction | Vector | tuple[int, int]
) -> Callable[[Vector], Iterable[Vector]]: ...
def make_direction_ranges(
    height: int, width: int, *directions: Direction | Vector | tuple[int, int]
) -> tuple[Callable[[Vector], Iterable[Vector]], ...]: ...

LETTER_LOOKUP = ...

LETTER_WIDTH: int = 4
LETTER_HEIGHT: int = 6
LETTER_COUNT: int = 8

def convert_letters(board: Iterable[bool]) -> str: ...
