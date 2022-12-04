def run(input_data):
    basement_position = accum = 0
    for position, char in enumerate(input_data, 1):
        if char == "(":
            accum += 1
        elif char == ")":
            accum -= 1

        if not basement_position and accum == -1:
            basement_position = position

    yield accum
    yield basement_position
