from __future__ import annotations


def process_line(line):
    command, _, count = line.partition(" ")
    count = int(count)
    return command, count


def run(input_data):
    x = depth = 0
    for command, count in input_data:
        if command == "forward":
            x += count
        elif command == "down":
            depth += count
        elif command == "up":
            depth -= count

    yield x * depth

    x = depth = aim = 0
    for command, count in input_data:
        if command == "forward":
            x += count
            depth += aim * count
        elif command == "down":
            aim += count
        elif command == "up":
            aim -= count

    yield x * depth
