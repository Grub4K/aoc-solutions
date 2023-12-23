from __future__ import annotations


def process_data(lines):
    from collections import Counter

    counter_dict = Counter(map(int, lines[0].split(",")))
    return [counter_dict.get(index, 0) for index in range(9)]


def run(fish_counter):
    from_ = 0
    to = 6

    for index in range(256):
        to = (to + 1) % 9
        fish_counter[to] += fish_counter[from_]
        from_ = (from_ + 1) % 9
        if index == 79:
            yield sum(fish_counter)

    yield sum(fish_counter)
