from utils import first, nwise


def process_data(data):
    return data[0]


def are_unique_items(sequence):
    return len(sequence) == len(set(sequence))


def run(data: list[str]):
    for size in 4, 14:
        yield first(
            index + size
            for index, items in enumerate(nwise(data, size))
            if are_unique_items(items)
        )
