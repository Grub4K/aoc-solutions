from queue import Queue


def process_line(line):
    return list(map(int, line))


def run(data):
    y_range = range(len(data))
    x_range = range(len(data[0]))

    shifts = set()
    for x_shift in [-1, 0, 1]:
        for y_shift in [-1, 0, 1]:
            shifts.add((x_shift, y_shift))
    shifts.remove((0, 0))

    def run_round():
        has_flashed = set()
        queue = Queue()

        for y in y_range:
            for x in x_range:
                point = x, y
                queue.put(point)

        while not queue.empty():
            point = queue.get(block=False)
            if point in has_flashed:
                continue

            x, y = point

            if data[y][x] == 9:
                has_flashed.add(point)

                # Add to the queue
                for x_shift, y_shift in shifts:
                    x_new = x + x_shift
                    y_new = y + y_shift
                    if x_new in x_range and y_new in y_range:
                        queue.put((x_new, y_new))
            else:
                data[y][x] += 1

        for x, y in has_flashed:
            data[y][x] = 0
        return len(has_flashed)

    flashes = 0
    all_flashed = False
    current_round = 0
    while current_round < 100 or not all_flashed:
        current_round += 1
        flashes += run_round()

        if sum(sum(line) for line in data) == 0:
            all_flashed = current_round

    yield flashes
    yield all_flashed
