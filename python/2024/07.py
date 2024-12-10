from __future__ import annotations

import enum
import itertools
import math


class Operation(enum.Enum):
    Add = enum.auto()
    Multiply = enum.auto()
    Concatenate = enum.auto()


def process_line(line: str) -> tuple[int, tuple[int, ...]]:
    target, _, nums = line.partition(": ")
    return int(target), tuple(map(int, nums.split()))


def run(data: list[tuple[int, tuple[int, ...]]]):
    part_a = 0
    part_b = 0

    for target, numbers in data:
        for operations in itertools.product(
            (Operation.Add, Operation.Multiply, Operation.Concatenate),
            repeat=len(numbers) - 1,
        ):
            result = numbers[0]

            for number, operation in zip(numbers[1:], operations):
                if result > target:
                    break

                if operation is Operation.Concatenate:
                    result = result * 10 ** (int(math.log10(number)) + 1) + number

                elif operation is Operation.Add:
                    result += number

                elif operation is Operation.Multiply:
                    result *= number

            if result == target:
                if Operation.Concatenate not in operations:
                    part_a += target
                part_b += target
                break

    yield part_a
    yield part_b
