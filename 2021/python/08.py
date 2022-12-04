UNIQUE_LENGTHS = [
    (1, 2),
    (4, 4),
    (7, 3),
    (8, 7),
]


def filter_wire(probes, wires):
    return {probe for probe in probes if probe.issuperset(wires)}


def solve_five_segments(probes, trans):
    three = filter_wire(probes, trans[1])
    probes ^= three
    five = filter_wire(probes, trans[4] ^ trans[1])
    two = probes ^ five
    return two.pop(), three.pop(), five.pop()


def solve_six_segments(probes, trans):
    remaining = filter_wire(probes, trans[1])
    six = probes ^ remaining
    nine = filter_wire(remaining, trans[4])
    zero = remaining ^ nine
    return zero.pop(), six.pop(), nine.pop()


def filter_length(probes, length):
    return {wires for wires in probes if len(wires) == length}


def find_numbers(data):
    for probes, outputs in data:
        filter_func = lambda length: filter_length(probes, length)
        trans = {}
        for value, segments in UNIQUE_LENGTHS:
            trans[value] = filter_func(segments).pop()
        trans[2], trans[3], trans[5] = solve_five_segments(filter_func(5), trans)
        trans[0], trans[6], trans[9] = solve_six_segments(filter_func(6), trans)
        translation = {
            frozenset(lookup): str(number) for number, lookup in trans.items()
        }

        yield int("".join(translation[output] for output in outputs))


def process_line(line):
    def process(dataset):
        return tuple(frozenset(wires) for wires in dataset.split(" "))

    probe, _, output = line.rstrip().partition(" | ")
    return process(probe), process(output)


def run(data):
    _, lengths = zip(*UNIQUE_LENGTHS)
    yield sum(1 for _, values in data for value in values if len(value) in lengths)
    yield sum(find_numbers(data))
