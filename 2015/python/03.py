from collections import Counter
from itertools import pairwise

with open("../input/03.txt") as file:
    data = file.read()


def create_positions(data):
    positions = Counter()
    x = y = 0

    positions.update([(x, y)])
    for direction in data:
        if direction == ">":
            x += 1
        elif direction == "<":
            x -= 1
        elif direction == "^":
            y += 1
        elif direction == "v":
            y -= 1

        positions.update([(x, y)])

    return positions

print(len(create_positions(data)))

positions = create_positions(data[::2])
positions.update(create_positions(data[1::2]))
print(len(positions))
