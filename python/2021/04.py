from __future__ import annotations

from utils import flatten
from utils import grouped


def is_winning(board, drawn):
    lines = (*grouped(board, 5), *zip(*grouped(board, 5)))
    return any(all(number in drawn for number in line) for line in lines)


def process_data(data):
    data_iterator = iter(data)
    draws = list(map(int, next(data_iterator).split(",")))

    boards = [list(map(int, flatten(map(str.split, lines)))) for lines in grouped(data_iterator, 6)]

    return draws, boards


def run(input_data):
    draws, boards = input_data

    drawn = set()
    win_values = []
    for draw in draws:
        drawn.add(draw)

        for board in boards:
            if not is_winning(board, drawn):
                continue
            board_without_drawn = {*board} - drawn
            board_value = sum(board_without_drawn) * draw
            win_values.append(board_value)
            boards.remove(board)
        if not boards:
            break

    yield win_values[0]
    yield win_values[-1]
