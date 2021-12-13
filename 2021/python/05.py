from collections import defaultdict
from collections import namedtuple



Point = namedtuple('Point', ['X', 'Y'])


def parse_line(line):
    def to_point(in_str):
        x, _, y = in_str.partition(',')
        return Point(int(x), int(y))

    from_str, _, to_str = line.partition(' -> ')
    return (to_point(from_str), to_point(to_str))


def make_range(a, b):
    step = 1 if a<=b else -1
    return range(a, b+step, step)


def calculate_intersections(lines, process_diagonals):
    points = defaultdict(int)
    for from_, to in lines:
        # Compute diagonals
        if from_.X != to.X and from_.Y != to.Y:
            if process_diagonals:
                x_range = make_range(from_.X, to.X)
                y_range = make_range(from_.Y, to.Y)
                for x, y in zip(x_range, y_range):
                    points[(x, y)] += 1
        # Compute verticals
        elif from_.X == to.X:
            for y in make_range(from_.Y, to.Y):
                point = (to.X, y)
                points[point] += 1
        # Compute horizontal
        elif from_.Y == to.Y:
            for x in make_range(from_.X, to.X):
                point = (x, to.Y)
                points[point] += 1
    # Count of values above 1 (number of intersections)
    return sum(1 for value in points.values() if value > 1)


with open('../input/05.txt') as file:
    lines = [*map(parse_line, file)]

print(calculate_intersections(lines, False))
print(calculate_intersections(lines, True))
