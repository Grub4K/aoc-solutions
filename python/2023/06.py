from __future__ import annotations

import math
from functools import reduce
from operator import mul


def process_line(line: str):
    return line.split()[1:]


def run_single(data: list[str]):
    time, distance = map(int, data)
    sqrt = math.isqrt(time**2 - 4 * distance - 1)
    return sqrt + ((sqrt ^ time ^ 1) & 1)


def run(data: list[list[str]]):
    yield reduce(mul, map(run_single, zip(*data)), 1)
    yield run_single(map("".join, data))
