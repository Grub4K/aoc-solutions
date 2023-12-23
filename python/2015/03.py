from __future__ import annotations

from collections import Counter


def yield_positions(data):
    x = y = 0
    yield (x, y)

    for direction in data:
        if direction == ">":
            x += 1
        elif direction == "<":
            x -= 1
        elif direction == "^":
            y += 1
        elif direction == "v":
            y -= 1

        yield (x, y)


def run(data):
    data = data[0]

    yield len(Counter(yield_positions(data)))

    positions = Counter(yield_positions(data[::2]))
    positions.update(yield_positions(data[1::2]))
    yield len(positions)
