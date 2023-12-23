from __future__ import annotations

from collections import deque
from collections import namedtuple

from utils import CARDINAL_DIRECTIONS
from utils import Vector
from utils import range2d


Node = namedtuple("Node", ["position", "height", "distance"])


def process_data(data: list[str]):
    start_pos = None
    end_pos = None

    width = len(data[0])
    height = len(data)

    grid = []
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "S":
                start_pos = Vector(x, y)
                elevation = 0
            elif char == "E":
                end_pos = Vector(x, y)
                elevation = 25
            else:
                elevation = ord(char) - 97

            grid.append(elevation)

    return start_pos, end_pos, width, height, grid


def run(data: tuple[Vector, Vector, int, int, list[int]]):
    start_pos, end_pos, width, height, grid = data

    def dijkstra(start_node: Node, end_condition, rev=False):
        length = width * height
        distances = [length] * length
        distances[start_node.position.y * width + start_node.position.x] = 0
        unvisited = set(map(Vector, range2d(width, height)))

        queue = deque([start_node])
        while queue:
            current = queue.popleft()
            if current.position not in unvisited:
                continue

            for direction in CARDINAL_DIRECTIONS:
                next_pos = current.position + direction.value
                if next_pos not in unvisited:
                    continue

                index = next_pos.y * width + next_pos.x
                next_height = grid[index]
                if rev:
                    if next_height + 1 < current.height:
                        continue
                elif next_height > current.height + 1:
                    continue

                new_distance = current.distance + 1
                if distances[index] > new_distance:
                    distances[index] = new_distance

                next_node = Node(next_pos, next_height, new_distance)
                if end_condition(next_node):
                    return next_node

                queue.append(next_node)

            unvisited.remove(current.position)

        raise RuntimeError("Never reached if valid solution exists")

    yield dijkstra(Node(start_pos, 0, 0), lambda c: c.position == end_pos).distance
    yield dijkstra(Node(end_pos, 25, 0), lambda c: c.height == 0, rev=True).distance
