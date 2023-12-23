from __future__ import annotations

import string


LOOKUP = dict(zip(string.ascii_letters, range(1, 26 * 2 + 1)))


def grouped(iterable, n):
    return zip(*[iter(iterable)] * n)


def run(data: list[str]):
    accum = 0
    for line in data:
        half = len(line) // 2
        common_element = set(line[:half]).intersection(line[half:]).pop()
        accum += LOOKUP[common_element]
    yield accum

    GROUP_SIZE = 3
    yield sum(
        LOOKUP[set(first).intersection(*group).pop()] for first, *group in grouped(data, GROUP_SIZE)
    )
