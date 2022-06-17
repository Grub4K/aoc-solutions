with open("../input/07.txt") as file:
    line = file.readline()

values = [*map(int, line.split(","))]
value_range = range(min(values), max(values) + 1)


def distance(a):
    return lambda b: abs(a - b)


print(min(sum(map(distance(a), values)) for a in value_range))


def fuel_distance(a):
    def _fuel(b):
        n = abs(a - b)
        return n * (n + 1) // 2

    return _fuel


print(min(sum(map(fuel_distance(a), values)) for a in value_range))
