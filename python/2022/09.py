from __future__ import annotations

import math

from utils import Direction
from utils import Vector
from utils import flatten

LOOKUP = {
    "R": Direction.RIGHT,
    "U": Direction.UP,
    "L": Direction.LEFT,
    "D": Direction.DOWN,
}


def process_line(line):
    direction, _, amount = line.partition(" ")
    return [LOOKUP[direction].value] * int(amount)


def process_data(data):
    return list(flatten(data))


def move_knots(knots, movement):
    previous = None
    for knot in knots:
        if previous is None:
            knot += movement
        else:
            delta = previous - knot
            if abs(delta.x) > 1 or abs(delta.y) > 1:
                knot += (
                    Vector(tuple(int(math.copysign(1, value)) for value in delta))
                    if delta.x and delta.y
                    else delta // 2
                )

        yield knot
        previous = knot


def run(movements: list[Vector]):
    for length in 2, 10:
        positions = set()
        knots = [Vector()] * length
        for movement in movements:
            knots = list(move_knots(knots, movement))
            positions.add(knots[-1])

        yield len(positions)
