from __future__ import annotations

import subprocess

from aoc.run import BASE_PATH
from aoc.run import Error
from aoc.run import RunInfo

MAIN_FILE = str(BASE_PATH / "zig/src/main.zig")


def run(run_infos: list[RunInfo]):
    args = ["zig", "run", MAIN_FILE, "--"]

    for run_info in run_infos:
        args.append(run_info.id.partition("-")[2])
        args.append(str(run_info.parts))
        args.append(str(run_info.input))

    process = subprocess.Popen(args, stdout=subprocess.PIPE, text=True)
    assert process.stdout
    for line in map(str.strip, process.stdout):
        if line.startswith("err"):
            yield Error(line.removeprefix("err, "))
            continue

        yield tuple(line.split(", ")[1:])
