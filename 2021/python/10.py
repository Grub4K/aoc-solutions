from queue import LifoQueue



with open('../input/10.txt') as file:
    data = [line.strip() for line in file]

syntax_values = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
completion_values = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}
brace_lookup = dict(zip('([{<', ')]}>'))


completion_scores = []
syntax_error_score = 0
for line in data:
    stack = LifoQueue()
    for char in line:
        if char in brace_lookup:
            stack.put(brace_lookup[char])
        else:
            if stack.get(block=False) != char:
                syntax_error_score += syntax_values[char]
                break
    else:
        if not stack.empty():
            completion_score = 0
            while not stack.empty():
                completion_score *= 5
                completion_score += completion_values[stack.get()]
            completion_scores.append(completion_score)

print(syntax_error_score)

completion_scores.sort()
middle_score = completion_scores[(len(completion_scores))//2]

print(middle_score)

