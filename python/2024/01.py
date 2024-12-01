from __future__ import annotations

import collections


def process_line(line: str):
    return tuple(map(int, line.split()))


def run(data: list[tuple[int, int]]):
    a, b = map(sorted, zip(*data))
    yield sum(abs(first - second) for first, second in zip(a, b))

    counter = collections.Counter(b)
    yield sum(number * counter.get(number, 0) for number in a)
