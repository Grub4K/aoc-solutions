import re
from functools import cmp_to_key
from itertools import zip_longest

from utils import first, flatten, grouped

NUMBER_PATTERN = re.compile(r"\d+")


def convert_single(line):
    index = 1

    result = []
    items = [result]

    while items:
        char = line[index]
        if char == "[":
            current = []
            items[-1].append(current)
            items.append(current)

        elif char == "]":
            items.pop()

        elif char != ",":
            match = NUMBER_PATTERN.match(line, index)
            assert match
            number = match.group()
            items[-1].append(int(number))
            index += len(number)
            continue

        index += 1

    return result


def process_data(data):
    return [
        (convert_single(first), convert_single(second))
        for first, second in grouped(filter(None, data), 2)
    ]


def deep_compare(a, b) -> int:
    if a is None:
        return -1
    if b is None:
        return 1
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    if isinstance(a, int):
        a = [a]
    elif isinstance(b, int):
        b = [b]

    return first(filter(None, (deep_compare(a, b) for a, b in zip_longest(a, b))), 0)


def run(data):
    yield sum(
        index
        for index, (first, second) in enumerate(data, 1)
        if deep_compare(first, second) < 0
    )

    a, b = [[2]], [[6]]
    sorted_data = sorted(flatten(data + [(a, b)]), key=cmp_to_key(deep_compare))
    yield (sorted_data.index(a) + 1) * (sorted_data.index(b) + 1)
