from __future__ import annotations

from collections import defaultdict
from heapq import nsmallest
from pathlib import PurePosixPath as Path

HOME_PATH = Path("/")
NEEDED_SPACE = 30_000_000
AVAILABLE_SPACE = 70_000_000


def process_data(data: list[str]) -> defaultdict[Path, list[Path | int]]:
    current_dir = HOME_PATH
    directories = defaultdict(list)

    for line in data:
        if line.startswith("$ cd "):
            directory = line.removeprefix("$ cd ")
            if directory == "..":
                current_dir = current_dir.parent
            elif directory == "/":
                current_dir = HOME_PATH
            else:
                current_dir /= directory
            continue

        if line.startswith("$"):
            continue

        size, _, name = line.partition(" ")
        result = (current_dir / name) if size == "dir" else int(size)
        directories[current_dir].append(result)

    return directories


def run(directories: dict[Path, list[Path | int]]):
    def get_value(item):
        return item if isinstance(item, int) else sizes.get(item)

    # Calculate sizes for each directory path
    sizes: dict[Path, int] = {}
    while directories:
        for directory, items in list(directories.items()):
            values = list(map(get_value, items))
            if all(values):
                sizes[directory] = sum(values)
                del directories[directory]

    yield sum(size for size in sizes.values() if size <= 100_000)

    required_space = sizes[HOME_PATH] + NEEDED_SPACE - AVAILABLE_SPACE
    yield from nsmallest(1, (item for item in sizes.values() if item > required_space))
