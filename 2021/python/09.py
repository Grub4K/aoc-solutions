from heapq import nlargest
from queue import Queue

SHIFTS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


with open("../input/09.txt") as file:
    data = [[*map(int, line.strip())] for line in file]

y_range = range(len(data))
x_range = range(len(data[0]))

points = {(x, y) for y in y_range for x in x_range if data[y][x] != 9}

queue = Queue()

risk_levels = []
basin_counts = []

while points:
    basin_counts.append(1)
    next_point = next(iter(points))
    points.remove(next_point)
    queue.put(next_point)

    while not queue.empty():
        x, y = queue.get()

        current = data[y][x]
        is_smaller = True
        for x_shift, y_shift in SHIFTS:
            x_shifted, y_shifted = test_point = (x + x_shift, y + y_shift)
            # Task 1
            if x_shifted in x_range and y_shifted in y_range:
                if current >= data[y_shifted][x_shifted]:
                    is_smaller = False
            # Task 2
            if test_point in points:
                queue.put(test_point)
                points.remove(test_point)
                basin_counts[-1] += 1

        if is_smaller:
            risk_levels.append(current + 1)

print(sum(risk_levels))

largest = nlargest(3, basin_counts)
print(largest[0] * largest[1] * largest[2])
