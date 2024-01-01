from __future__ import annotations

import re


def process_line(line: str) -> str:
    result = []
    for chunk in re.split(r", |; ", line.partition(": ")[2]):
        num, _, color = chunk.partition(" ")
        result.append((int(num), color))

    return result


def get_required_cubes(game: list[tuple[int, str]]):
    red = green = blue = 0

    for count, color in game:
        if color == "red":
            red = max(red, count)
        elif color == "green":
            green = max(green, count)
        elif color == "blue":
            blue = max(blue, count)

    return red, green, blue


def run(data: list[list[tuple[int, str]]]):
    required_cubes = list(map(get_required_cubes, data))

    yield sum(
        index
        for index, (r, g, b) in enumerate(required_cubes, 1)
        if r <= 12 and g <= 13 and b <= 14
    )

    yield sum(r * g * b for r, b, g in required_cubes)
