from collections import defaultdict


def process_data(data):
    paths = defaultdict(set)
    for line in data:
        key, _, value = line.rstrip().partition("-")
        paths[key].add(value)
        paths[value].add(key)

    return paths


def find_paths(paths, budget):
    def _find_paths(state, visited, budget):
        if state.islower():
            visited = visited | {state}

        accum = 0
        for new_state in paths[state]:
            if new_state == "end":
                accum += 1
                continue

            if new_state == "start":
                continue

            new_small_budget = budget
            if new_state in visited:
                if not budget:
                    continue
                new_small_budget -= 1

            accum += _find_paths(new_state, visited, new_small_budget)

        return accum

    return _find_paths("start", set(), budget)


def run(paths):
    yield find_paths(paths, 0)
    yield find_paths(paths, 1)
