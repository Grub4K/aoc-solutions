from __future__ import annotations

from utils import nwise


def process(data, grouplength):
    sum_of_n = list(map(sum, nwise(data, grouplength)))

    count = 0
    for first, second in nwise(sum_of_n, 2):
        if second > first:
            count += 1

    return count


process_line = int


def run(input_data):
    yield process(input_data, 1)
    yield process(input_data, 3)
