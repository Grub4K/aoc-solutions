from __future__ import annotations

from itertools import count

from utils import flatten
from utils import nwise


def parse_point(point):
    a, _, b = point.partition(",")
    return int(a), int(b)


def point_range(a: tuple[int, int], b: tuple[int, int]):
    if a[0] != b[0]:
        assert a[1] == b[1]
        start, end = min(a[0], b[0]), max(a[0], b[0]) + 1
        for x in range(start, end):
            yield x, a[1]

        return

    assert a[0] == b[0]
    assert a[1] != b[1]
    start, end = min(a[1], b[1]), max(a[1], b[1]) + 1
    for y in range(start, end):
        yield a[0], y


def process_line(line: str):
    lines = nwise((parse_point(point) for point in line.split(" -> ")), 2)
    yield from flatten(point_range(a, b) for a, b in lines)


def process_data(data: list[list[tuple[int, int]]]):
    return set(flatten(data))


def simulate(obstructions: set[tuple[int, int]], limit: int):
    start_point = 500, 0

    for amount in count():
        current_x, current_y = start_point

        while ...:
            new_y = current_y + 1
            for offset_x in (0, -1, 1):
                new = (current_x + offset_x, new_y)
                if new not in obstructions:
                    if new_y == limit:
                        return amount
                    current_x, current_y = new
                    break

            else:
                if current_y == 0:
                    return amount + 1

                obstructions.add((current_x, current_y))
                break

    raise


def run(obstructions: set[tuple[int, int]]):
    limit = max(obstructions, key=lambda a: a[1])[1]
    result = simulate(obstructions, limit)
    yield result

    # Add floor and keep going
    limit += 2
    obstructions.update(point_range((300, limit), (700, limit)))
    yield simulate(obstructions, limit) + result
