from __future__ import annotations

import subprocess

from aoc.run import BASE_PATH
from aoc.run import Error
from aoc.run import RunInfo

BASH_BASE = BASE_PATH / "bash/"


def run(run_infos: list[RunInfo]):
    for run_info in run_infos:
        name = run_info.id.partition("-")[2].replace("-", "/") + ".sh"

        process = subprocess.run(
            [str(BASH_BASE / name), str(run_info.input)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if process.returncode:
            yield Error(f"returncode {process.returncode}: {process.stderr}")
            continue

        a, *b = process.stdout.split()
        yield a, b[0] if b else None
