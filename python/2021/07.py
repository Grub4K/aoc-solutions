def process_data(lines):
    return [*map(int, lines[0].split(","))]


def normal_distance(a):
    return lambda b: abs(a - b)


def fuel_distance(a):
    def fuel(b):
        n = abs(a - b)
        return n * (n + 1) // 2

    return fuel


def run(input_data):
    value_range = range(min(input_data), max(input_data) + 1)

    for distance in normal_distance, fuel_distance:
        yield min(sum(map(distance(a), input_data)) for a in value_range)
