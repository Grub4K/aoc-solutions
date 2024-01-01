from __future__ import annotations

from collections import namedtuple

Range = namedtuple("Range", ["start", "stop"])


def process_line(line):
    def make_range(elf):
        start, _, stop = elf.partition("-")
        return Range(int(start), int(stop))

    first, _, second = line.partition(",")
    return make_range(first), make_range(second)


def run(data):
    count_a = count_b = 0
    for a, b in data:
        if a.start <= b.start and b.stop <= a.stop or b.start <= a.start and a.stop <= b.stop:
            count_a += 1

        if b.start <= a.stop and a.start <= b.stop or a.start <= b.stop and b.start <= a.stop:
            count_b += 1

    yield count_a
    yield count_b
