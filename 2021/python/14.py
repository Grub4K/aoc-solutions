from collections import Counter


def process_data(data):
    def process_rule(line):
        key, _, value = line.partition(" -> ")
        return tuple(key), value

    polymer = data[0]
    rules = dict(process_rule(rule) for rule in data[2:])

    return polymer, rules


def update(transitions, rules):
    updates = Counter()
    for (x, y), count in transitions.items():
        a = rules.get((x, y))
        if a is None:
            continue

        updates[(x, a)] += count
        updates[(a, y)] += count
        updates[(x, y)] -= count

    transitions.update(updates)
    # Clear entries that have `0` as a count
    transitions = +transitions


def calculate_result(transitions):
    counts = Counter()

    for (a, _), count in transitions.items():
        counts[a] += count

    quantities = [*counts.values()]
    return max(quantities) - min(quantities)


def run(data):
    polymer, rules = data

    transitions = Counter(zip(polymer, polymer[1:]))
    # We only count the first letter of the transition pair
    # so we need to add the last letter explicitly
    transitions[(polymer[-1], "")] += 1

    for _ in range(10):
        update(transitions, rules)
    yield calculate_result(transitions)

    for _ in range(40 - 10):
        update(transitions, rules)
    yield calculate_result(transitions)
