from __future__ import annotations

import heapq


def process_data(lines):
    result = [0]
    for line in lines:
        if not line:
            result.append(0)
            continue

        result[-1] += int(line)

    return result


def run(data_input):
    largest = heapq.nlargest(3, data_input)
    yield largest[0]
    yield sum(largest)
