from __future__ import annotations

import importlib.util
import sys

from dataclasses import dataclass
from pathlib import Path


BASE_PATH = Path(__file__, "../..").resolve()


@dataclass
class RunInfo:
    name: str
    year: str
    day: str
    input: Path  # noqa: A003
    parts: int

    @property
    def id(self):  # noqa: A003
        return f"{self.name}-{self.year}-{self.day}"


@dataclass
class Error:
    message: str


def relative(path: Path):
    return path.relative_to(BASE_PATH).as_posix()


def import_file(file: Path, name: str | None = None):
    if not name:
        name = file.stem

    spec = importlib.util.spec_from_file_location(name, file)

    if not spec or not spec.loader:
        raise ImportError(f"Could not import {relative(file)}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod


def _resolve(name: str, pattern: str, test: bool):
    year, _, day = pattern.partition("-")
    day, _, part = day.partition("-")

    year = year or "*"
    day = day.zfill(2) if day else "*"
    parts = {
        "a": 0b01,
        "1": 0b01,
        "b": 0b10,
        "2": 0b10,
    }.get(part, 0b11)

    for path in BASE_PATH.glob(f"{name}/{year}/{day}.*"):
        year = path.parent.name
        day = path.stem
        if not year.isdecimal() or not day.isdecimal():
            continue

        suffix = "#" if test else ""
        input_path = BASE_PATH / f"input/{year}/{day}{suffix}.txt"
        if input_path.is_file():
            yield year, day, input_path, parts
            continue

        print(
            f"{name}-{year}-{day}: ERROR: missing input file: {relative(input_path)}",
            file=sys.stderr,
        )


def execute_runner(name: str, patterns: list[str], test: bool):
    runner = import_file(BASE_PATH / f"{name}/runner.py")

    runs: dict[tuple[str, str, Path], RunInfo] = {}
    for pattern in patterns:
        for year, day, input_path, parts in _resolve(name, pattern, test):
            key = (year, day, input_path)
            if key in runs:
                runs[key].parts |= parts
            else:
                runs[key] = RunInfo(name, year, day, input_path, parts)

    run_list = [run for _, run in sorted(runs.items())]
    for run, result in zip(run_list, runner.run(run_list), strict=True):
        if isinstance(result, Error):
            print(f"{run.id}: ERROR: {result.message}", file=sys.stderr)
            continue

        for part, result in zip("12", result, strict=True):
            if result is None:
                continue

            if isinstance(result, Error):
                error = "No result" if result is None else result.message
                print(f"{run.id}-{part}: ERROR: {error}", file=sys.stderr)

            else:
                print(f"{run.id}-{part}: {result}")


def get_runners():
    return sorted(path.parent.name for path in BASE_PATH.glob("*/runner.py"))


RUNNERS = get_runners()
