from __future__ import annotations

import math
from functools import reduce
from operator import mul


def process_line(line: str):
    return line.split()[1:]


def run_single(time: str, distance: str):
    time = int(time)
    sqrt = math.isqrt(time**2 - 4 * int(distance) - 1)
    return sqrt + ((sqrt ^ time ^ 1) & 1)


def run(data: list[list[int]]):
    times, distances = data

    yield reduce(mul, map(run_single, times, distances), 1)
    yield run_single("".join(times), "".join(distances))
