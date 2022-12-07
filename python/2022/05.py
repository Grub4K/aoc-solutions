from collections import defaultdict, namedtuple

Movement = namedtuple("Movement", ["count", "from_", "to"])


def process_data(lines: list[str]):
    iterator = iter(lines)

    index = 0
    box_lookup = defaultdict(list)
    while True:
        line = next(iterator)[1::4]
        if line.isnumeric():
            next(iterator)
            break

        for index, char in enumerate(line, 1):
            if char == " ":
                continue

            box_lookup[index].append(char)

    boxes = [box_lookup[i] for i in range(1, index + 1)]
    for stack in boxes:
        stack.reverse()

    movements = [
        Movement(int(line_info[0]), int(line_info[1]) - 1, int(line_info[2]) - 1)
        for line_info in (line.split()[1::2] for line in iterator)
    ]

    return boxes, movements


def work(boxes, movements, reverse=False):
    for movement in movements:
        append = boxes[movement.from_][-movement.count :]
        boxes[movement.to].extend(reversed(append) if reverse else append)
        del boxes[movement.from_][-movement.count :]


def run(data):
    base_boxes, movements = data

    for first in True, False:
        boxes = [stack.copy() for stack in base_boxes] if first else base_boxes
        work(boxes, movements, reverse=first)
        yield "".join(stack[-1] for stack in boxes)
