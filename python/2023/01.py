from __future__ import annotations

import re

NUMBERS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def make_number(a: re.Match | None, b: re.Match | None):
    assert a, "Input data invalid"
    assert b, "Input data invalid"
    return NUMBERS[a[1]] * 10 + NUMBERS[b[1]]


def run(data: list[str]):
    for numbers in "0123456789", NUMBERS:
        regex = "|".join(map(re.escape, numbers))
        begin = re.compile(f".*?({regex})").match
        end = re.compile(f".*({regex}).*?").fullmatch

        yield sum(make_number(begin(line), end(line)) for line in data)
