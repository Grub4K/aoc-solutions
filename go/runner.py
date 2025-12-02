from __future__ import annotations

import json
import subprocess

from aoc.run import BASE_PATH
from aoc.run import Error

TYPE_CHECKING = False
if TYPE_CHECKING:
    from aoc.run import RunInfo


def run(run_infos: list[RunInfo]):
    args = ["go", "run", "."]

    for run_info in run_infos:
        args.append(str(run_info.year))
        args.append(str(run_info.day))
        args.append(str(run_info.input))

    process = subprocess.Popen(
        args,
        cwd=BASE_PATH / "go",
        stdout=subprocess.PIPE,
        text=True,
    )
    assert process.stdout
    for line in map(str.strip, process.stdout):
        type_, _, payload = line.partition(":")
        payload = json.loads(payload)
        if type_ == "error":
            yield Error(payload)
            continue

        assert type_ == "value"
        yield tuple(payload)
