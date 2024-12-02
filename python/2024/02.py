from __future__ import annotations

import utils


def process_line(line: str):
    return list(map(int, line.split()))


def is_safe(line: list[int]):
    allowed_differences = None

    for a, b in utils.nwise(line, 2):
        if allowed_differences is None:
            allowed_differences = (1, 2, 3) if a < b else (-1, -2, -3)

        if (b - a) not in allowed_differences:
            return False

    return True


def windows(line: list[int]):
    for index, _ in enumerate(line):
        yield line[:index] + line[index + 1 :]


def run(data: list[list[int]]):
    yield sum(map(is_safe, data))
    yield sum(any(map(is_safe, windows(line))) for line in data)
