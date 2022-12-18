from collections import namedtuple

from utils import CARDINAL_DIRECTIONS, Vector, make_direction_ranges, range2d


def process_line(line):
    return list(map(int, line))


Result = namedtuple("Result", ["scenic_score", "visible"])


def run(data: list[list[int]]):
    height = len(data)
    width = len(data[0])

    up, down, left, right = make_direction_ranges(height, width, *CARDINAL_DIRECTIONS)

    def calculate_slice(range_, tree):
        visible = True
        scenic_score = 0
        for position in range_:
            scenic_score += 1

            if data[position.y][position.x] >= tree:
                visible = False
                break

        return Result(scenic_score, visible)

    def process_tree(position):
        position = Vector(position)
        tree = data[position.y][position.x]

        visible = False
        scenic_score = 1
        for direction_range in up, down, left, right:
            result = calculate_slice(direction_range(position), tree)

            visible |= result.visible
            scenic_score *= result.scenic_score

        return Result(scenic_score, visible)

    results = list(map(process_tree, range2d(width, height)))
    yield sum(result.visible for result in results)
    yield max(result.scenic_score for result in results)
