from collections import defaultdict

paths = defaultdict(set)
with open("../input/12.txt") as file:
    for line in file:
        key, _, value = line.rstrip().partition("-")
        paths[key].add(value)
        paths[value].add(key)


def find_paths(budget):
    def _find_paths(state, visited, budget):
        if state.islower():
            visited.add(state)

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

            accum += _find_paths(new_state, visited.copy(), new_small_budget)

        return accum

    return _find_paths("start", set(), budget)


print(find_paths(0))
print(find_paths(1))
