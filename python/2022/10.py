from collections import namedtuple

from utils import convert_letters, flatten

Instruction = namedtuple("Instruction", ["cycles", "amount"])


def process_line(line):
    amount = line.partition(" ")[2]
    return (0, int(amount)) if amount else (0,)


def run(data: list[Instruction]):
    captured = range(20, 1000000, 40)  # Please don't judge lol

    x = 1
    result = 0
    for cycle, amount in enumerate(flatten(data), 1):
        if cycle in captured:
            result += x * cycle

        x += amount

    yield result

    WIDTH = 40
    HEIGHT = 6
    screen = [False] * (WIDTH * HEIGHT)

    x = 0
    for cycle, amount in enumerate(flatten(data)):
        mask = (x % WIDTH, (x + 1) % WIDTH, (x + 2) % WIDTH)
        if cycle % WIDTH in mask:
            screen[cycle] = True

        x += amount

    # Translate the screen to characters automatically
    yield convert_letters(screen)
