from __future__ import annotations

from queue import LifoQueue

SYNTAX_VALUES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
COMPLETION_VALUES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
BRACE_LOOKUP = dict(zip("([{<", ")]}>"))


def run(data):
    completion_scores = []
    syntax_error_score = 0
    for line in data:
        stack = LifoQueue()
        for char in line:
            if char in BRACE_LOOKUP:
                stack.put(BRACE_LOOKUP[char])
            else:
                if stack.get(block=False) != char:
                    syntax_error_score += SYNTAX_VALUES[char]
                    break
        else:
            if not stack.empty():
                completion_score = 0
                while not stack.empty():
                    completion_score *= 5
                    completion_score += COMPLETION_VALUES[stack.get()]
                completion_scores.append(completion_score)

    yield syntax_error_score

    completion_scores.sort()
    middle_score = completion_scores[(len(completion_scores)) // 2]

    yield middle_score
