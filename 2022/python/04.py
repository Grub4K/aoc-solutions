def process_line(line):
    def make_range(elf):
        from_, _, to = elf.partition("-")
        return set(range(int(from_), int(to) + 1))

    first, _, second = line.partition(",")
    return make_range(first), make_range(second)


def run(data: list[tuple[set[int], set[int]]]):
    yield sum(1 for a, b in data if a.issubset(b) or b.issubset(a))
    yield sum(1 for a, b in data if not a.isdisjoint(b))
