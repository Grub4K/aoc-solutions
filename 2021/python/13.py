from functools import reduce

THROWAWAY_POINT = -1, -1

LETTER_WIDTH = 4
LETTER_HEIGHT = 6
LETTER_COUNT = 8
# Flattened letter lookup for the decoding.
# INCOMPLETE! will output code if not found.
LETTER_LOOKUP = {
    0x699F99: "A",
    0x698896: "C",
    0xF8E888: "F",
    0x9ACAA9: "K",
    0x88888F: "L",
    0xE99E88: "P",
    0xE99EA9: "R",
    0x999996: "U",
    0xF1248F: "Z",
}


def make_fold(cont, instruction):
    pos, direction_x = instruction

    make_x_fold = (
        lambda x, y: THROWAWAY_POINT
        if x == pos
        else cont((pos * 2) - x, y)
        if x > pos
        else cont(x, y)
    )
    make_y_fold = (
        lambda x, y: THROWAWAY_POINT
        if y == pos
        else cont(x, (pos * 2) - y)
        if y > pos
        else cont(x, y)
    )

    return make_x_fold if direction_x else make_y_fold


def process_data(input_data: list[str]):
    instructions = []
    points = []
    for line in input_data:
        if not line:
            continue

        if line.startswith("fold along "):
            line = line[len("fold along ") :]
            direction, _, position = line.partition("=")
            instructions.append((int(position), direction == "x"))
        else:
            x, _, y = line.partition(",")
            points.append((int(x), int(y)))

    return instructions, points


def run(data):
    instructions, points = data

    fold_func = make_fold(lambda x, y: (x, y), instructions[0])
    points = set(map(lambda point: fold_func(*point), points))
    points.discard(THROWAWAY_POINT)
    yield len(points)

    fold_func = reduce(make_fold, reversed(instructions[1:]), lambda x, y: (x, y))
    points = set(map(lambda point: fold_func(*point), points))
    points.discard(THROWAWAY_POINT)

    result_width = LETTER_COUNT * (LETTER_WIDTH + 1)
    board = [["0" for _ in range(result_width)] for _ in range(LETTER_HEIGHT)]
    for x, y in points:
        board[y][x] = "1"

    result = ""
    for x in range(0, result_width, LETTER_WIDTH + 1):
        letter_code = int(
            "".join(
                c for y in range(LETTER_HEIGHT) for c in board[y][x : x + LETTER_WIDTH]
            ),
            base=2,
        )
        letter = LETTER_LOOKUP.get(letter_code)
        # If we cannot automatically decode the output, print the packed hex value
        result += letter if letter else f"({letter_code:X})"

    yield result
