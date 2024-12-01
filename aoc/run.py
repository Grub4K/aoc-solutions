from __future__ import annotations

import importlib.util
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

BASE_PATH = Path(__file__, "../..").resolve()
NUMBER_RE = re.compile(r"\d+")


@dataclass
class RunInfo:
    name: str
    year: str
    day: str
    input: Path
    parts: int

    @property
    def id(self):
        return f"{self.name}-{self.year}-{self.day}"


@dataclass
class Error:
    message: str
    traceback: str | None = None

    def __str__(self):
        if self.traceback:
            trace = textwrap.indent(self.traceback, "    ")
            return f"{self.message}\n{trace}"

        return self.message


def relative(path: Path):
    return path.relative_to(BASE_PATH).as_posix()


def import_file(file: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, file)

    if not spec or not spec.loader:
        raise ImportError(f"Could not import {relative(file)}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module


def _resolve(name: str, pattern: str, test: bool):
    year, _, day = pattern.partition("-")
    day, _, part = day.partition("-")

    day = f"*{day:0>2}" if day else "*"
    parts = {
        "a": 0b01,
        "1": 0b01,
        "b": 0b10,
        "2": 0b10,
    }.get(part, 0b11)

    for path in BASE_PATH.glob(f"{name}/**/*{year}/{day}.*"):
        year = NUMBER_RE.search(path.parent.name)
        day = NUMBER_RE.search(path.stem)
        if not year or not day:
            continue
        year, day = year[0], day[0]

        suffix = "#" if test else ""
        input_path = BASE_PATH / f"input/{year}/{day}{suffix}.txt"
        yield year, day, input_path, parts


def generate_runs(name: str, patterns: list[str], test: bool):
    runs: dict[tuple[str, str, Path], RunInfo] = {}
    for pattern in patterns:
        for year, day, input_path, parts in _resolve(name, pattern, test):
            key = (year, day, input_path)
            if key in runs:
                runs[key].parts |= parts
            else:
                runs[key] = RunInfo(name, year, day, input_path, parts)

    for _, run in sorted(runs.items()):
        if run.input.is_file():
            yield run
        else:
            print(
                f"{run.id}: ERROR: missing input: {relative(run.input)}",
                file=sys.stderr,
            )


def execute_runs(runner, runs: list[RunInfo]):
    if callable(getattr(runner, "run_single", None)):
        results = map(runner.run_single, runs)
    else:
        results = runner.run(runs)

    for run, result in zip(runs, results, strict=True):
        if isinstance(result, Error):
            print(f"{run.id}: ERROR: {result}", file=sys.stderr)
            continue

        for part, solution in zip([1, 2], result, strict=True):
            if not run.parts & part or solution is None:
                continue

            if isinstance(solution, Error):
                print(f"{run.id}-{part}: ERROR: {solution}", file=sys.stderr)

            else:
                print(f"{run.id}-{part}: {solution}")


def execute(name: str, patterns: list[str], test: bool):
    runner = import_file(BASE_PATH / f"{name}/runner.py", f"aoc.{name}.runner")
    runs = generate_runs(name, patterns, test)
    execute_runs(runner, list(runs))


RUNNERS = sorted(path.parent.name for path in BASE_PATH.glob("*/runner.py"))
