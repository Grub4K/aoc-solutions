from collections import Counter, namedtuple
from itertools import cycle


def process_line(line):
    Point = namedtuple("Point", ["X", "Y"])

    def to_point(in_str):
        x, _, y = in_str.partition(",")
        return Point(int(x), int(y))

    from_str, _, to_str = line.partition(" -> ")
    return to_point(from_str), to_point(to_str)


def make_range(a, b):
    return cycle([a]) if a == b else range(min(a, b), max(a, b) + 1)


def calculate_intersections(lines, process_diagonals):
    points = Counter()
    for from_, to in lines:
        if not process_diagonals:
            if from_.X != to.X and from_.Y != to.Y:
                continue

        x_range = make_range(from_.X, to.X)
        y_range = make_range(from_.Y, to.Y)
        points.update(zip(x_range, y_range))

    # Count of values above 1 (number of intersections)
    return sum(1 for value in points.values() if value > 1)


def run(input_data):
    yield calculate_intersections(input_data, False)
    yield calculate_intersections(input_data, True)
