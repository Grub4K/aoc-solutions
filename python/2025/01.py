from __future__ import annotations

import enum


class Direction(enum.Enum):
    Clockwise = enum.auto()
    Counterclockwise = enum.auto()


def process_line(line: str):
    direction = Direction.Clockwise if line[0] == "R" else Direction.Counterclockwise
    return direction, int(line[1:])


def run(data: list[tuple[Direction, int]]):
    dial = 50
    counter_a = 0
    counter_b = 0
    prev_direction = Direction.Clockwise

    for direction, movement in data:
        if direction != prev_direction:
            dial = (100 - dial) % 100
            prev_direction = direction

        rotations, dial = divmod(dial + movement, 100)
        counter_a += dial == 0
        counter_b += rotations


    yield counter_a
    yield counter_b
