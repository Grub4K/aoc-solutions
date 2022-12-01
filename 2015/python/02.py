def parse_line(line):
    a, b, c = line.split("x")
    return int(a), int(b), int(c)


def wrapping_paper(data):
    for length, width, height in data:
        sizes = (length * width, width * height, height * length)
        yield min(sizes) + 2 * sum(sizes)


def ribbon(data):
    for length, width, height in data:
        ribbon_base = length + width + height - max(length, width, height)
        yield 2 * ribbon_base + length * width * height


with open("../input/02.txt") as file:
    data = [parse_line(line) for line in file]

print(sum(wrapping_paper(data)))
print(sum(ribbon(data)))
