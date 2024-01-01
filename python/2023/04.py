from __future__ import annotations


def process_line(line: str):
    data = line.partition(": ")[2].split(" | ")
    winning, own = (list(map(int, chunk.split())) for chunk in data)
    return sum(number in winning for number in own)


def run(data: list[int]):
    yield sum((1 << (winning - 1)) for winning in data if winning)

    cards = [1] * len(data)
    for offset, (amount, winning) in enumerate(zip(cards, data), 1):
        for index in range(offset, offset + winning):
            cards[index] += amount

    yield sum(cards)
