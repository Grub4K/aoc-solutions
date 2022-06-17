def process_line(line):
    command, _, count = line.partition(" ")
    count = int(count)
    return command, count


with open("../input/02.txt") as file:
    data = list(map(process_line, file))

x = depth = 0
for command, count in data:
    if command == "forward":
        x += count
    elif command == "down":
        depth += count
    elif command == "up":
        depth -= count

print(x * depth)


x = depth = aim = 0
for command, count in data:
    if command == "forward":
        x += count
        depth += aim * count
    elif command == "down":
        aim += count
    elif command == "up":
        aim -= count

print(x * depth)
