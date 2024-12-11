from __future__ import annotations

import collections
import itertools

import utils


def run(data: list[str]):
    width = len(data[0])
    height = len(data)

    placements: dict[str, list[utils.Vector]] = collections.defaultdict(list)
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == ".":
                continue
            placements[char].append(utils.Vector(x, y))

    antinodes_a = set()
    antinodes_b = set()
    for char, antennas in placements.items():
        for first, second in itertools.combinations(antennas, 2):
            offset = second - first

            for multiplier in itertools.count():
                position = first - multiplier * offset
                if position.x not in range(width) or position.y not in range(height):
                    break
                if multiplier == 1:
                    antinodes_a.add(position)
                antinodes_b.add(position)

            for multiplier in itertools.count():
                position = second + multiplier * offset
                if position.x not in range(width) or position.y not in range(height):
                    break
                if multiplier == 1:
                    antinodes_a.add(position)
                antinodes_b.add(position)

    yield len(antinodes_a)
    yield len(antinodes_b)
