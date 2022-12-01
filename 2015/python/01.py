with open("../input/01.txt") as file:
    data = file.read()

basement_position = 0
accum = 0
for position, char in enumerate(data, 1):
    if char == "(":
        accum += 1
    elif char == ")":
        accum -= 1

    if not basement_position and accum == -1:
        basement_position = position

print(accum)
print(basement_position)
