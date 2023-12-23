from __future__ import annotations

import sys
import traceback

from aoc.run import RunInfo, Error, BASE_PATH, import_file

sys.path.insert(0, str(BASE_PATH/"python"))

def get_error(message: str = ""):
    if message:
        message = f"{message}: "

    error = sys.exc_info()[1]
    assert error is not None

    exception = traceback.format_exception_only(None, error)[-1].rstrip()
    return Error(f"{message}{exception}")


def run(runs: list[RunInfo]):
    for run in runs:
        run_path = BASE_PATH.joinpath("python", run.year, f"{run.day}.py")

        try:
            module = import_file(run_path, f"{run.year}.{run.day}")
        except Exception:
            yield get_error("Could not import file")
            continue

        input_data = run.input.read_text().splitlines(keepends=False)

        try:
            process_line = getattr(module, "process_line", None)
            if process_line:
                input_data = [process_line(line) for line in input_data]

            process_data = getattr(module, "process_data", None)
            if process_data:
                input_data = process_data(input_data)

        except Exception:
            yield get_error("Error processing input file")
            continue

        try:
            solutions = iter(module.run(input_data))
        except Exception:
            yield get_error("Error in run() function")
            continue

        try:
            first = next(solutions, None)
            yield (
                first if run.parts & 0b01 else None,
                next(solutions, None) if run.parts & 0b10 else None,
            )
        except Exception:
            yield get_error("Error while calculating solution")
