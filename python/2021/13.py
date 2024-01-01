from __future__ import annotations

from functools import reduce
from itertools import starmap

from utils import LETTER_COUNT
from utils import LETTER_HEIGHT
from utils import LETTER_WIDTH
from utils import convert_letters
from utils import range2d

THROWAWAY_POINT = -1, -1


def make_fold(cont, instruction):
    pos, direction_x = instruction

    make_x_fold = (  # noqa: E731
        lambda x, y: THROWAWAY_POINT
        if x == pos
        else cont((pos * 2) - x, y)
        if x > pos
        else cont(x, y)
    )
    make_y_fold = (  # noqa: E731
        lambda x, y: THROWAWAY_POINT
        if y == pos
        else cont(x, (pos * 2) - y)
        if y > pos
        else cont(x, y)
    )

    return make_x_fold if direction_x else make_y_fold


def process_data(input_data: list[str]):
    instructions = []
    points = []
    for line in input_data:
        if not line:
            continue

        if line.startswith("fold along "):
            line = line[len("fold along ") :]
            direction, _, position = line.partition("=")
            instructions.append((int(position), direction == "x"))
        else:
            x, _, y = line.partition(",")
            points.append((int(x), int(y)))

    return instructions, points


def run(data):
    instructions, points = data

    fold_func = make_fold(lambda x, y: (x, y), instructions[0])
    points = set(starmap(fold_func, points))
    points.discard(THROWAWAY_POINT)
    yield len(points)

    fold_func = reduce(make_fold, reversed(instructions[1:]), lambda x, y: (x, y))
    points = set(starmap(fold_func, points))
    points.discard(THROWAWAY_POINT)

    yield convert_letters(
        point in points for point in range2d((LETTER_WIDTH + 1) * LETTER_COUNT, LETTER_HEIGHT)
    )
