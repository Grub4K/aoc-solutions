from collections import Counter


def read_file(path):
    def process_rule(line):
        key, _, value = line.partition(" -> ")
        return tuple(key), value

    with open(path) as file:
        iterator = iter(map(str.rstrip, file))
        polymer = next(iterator)
        next(iterator)
        rules = dict(process_rule(rule) for rule in iterator)

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


polymer, rules = read_file("../input/14.txt")

transitions = Counter(zip(polymer, polymer[1:]))
# We only count the first letter of the transition pair
# so we need to add the last letter explicitly
transitions[(polymer[-1], "")] += 1

for _ in range(10):
    update(transitions, rules)
print(calculate_result(transitions))

for _ in range(40 - 10):
    update(transitions, rules)
print(calculate_result(transitions))
