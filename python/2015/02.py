from __future__ import annotations


def process_line(line):
    a, b, c = line.split("x")
    return int(a), int(b), int(c)


def wrapping_paper(data):
    for length, width, height in data:
        sizes = (length * width, width * height, height * length)
        yield min(sizes) + 2 * sum(sizes)


def ribbon(data):
    for length, width, height in data:
        ribbon_base = length + width + height - max(length, width, height)
        yield 2 * ribbon_base + length * width * height


def run(input_data):
    yield sum(wrapping_paper(input_data))
    yield sum(ribbon(input_data))
