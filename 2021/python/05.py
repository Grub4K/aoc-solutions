from collections import Counter, namedtuple

Point = namedtuple("Point", ["X", "Y"])


def parse_line(line):
    def to_point(in_str):
        x, _, y = in_str.partition(",")
        return Point(int(x), int(y))

    from_str, _, to_str = line.partition(" -> ")
    return (to_point(from_str), to_point(to_str))


def make_range(a, b):
    if a == b:
        while True:
            yield a

    yield from range(min(a, b), max(a, b) + 1)


def calculate_intersections(lines, process_diagonals):
    points = Counter()
    for from_, to in lines:
        if from_.X != to.X and from_.Y != to.Y:
            if not process_diagonals:
                continue

        x_range = make_range(from_.X, to.X)
        y_range = make_range(from_.Y, to.Y)
        points.update(zip(x_range, y_range))

    # Count of values above 1 (number of intersections)
    return sum(1 for value in points.values() if value > 1)


with open("../input/05.txt") as file:
    lines = [*map(parse_line, file)]

print(calculate_intersections(lines, False))
print(calculate_intersections(lines, True))
