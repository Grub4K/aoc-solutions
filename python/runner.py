from __future__ import annotations

import sys
import textwrap
import traceback

from aoc.run import BASE_PATH
from aoc.run import Error
from aoc.run import RunInfo
from aoc.run import import_file

sys.path.insert(0, str(BASE_PATH / "python"))


def get_error(error: Exception, message: str = "", stacklevel: int = 0):
    if message:
        message = f"{message}: "

    exception = traceback.format_exception_only(None, error)[-1].rstrip()
    summary = traceback.extract_tb(error.__traceback__)
    if stacklevel:
        summary = traceback.StackSummary.from_list(summary[stacklevel:])
    trace = textwrap.dedent("".join(summary.format()))

    return Error(f"{message}{exception}", trace)


def run_single(run_info: RunInfo):
    run_path = BASE_PATH.joinpath("python", run_info.year, f"{run_info.day}.py")

    try:
        module = import_file(run_path, f"aoc.python.{run_info.year}.{run_info.day}")
    except Exception as error:
        return get_error(error, "Could not import file", 4)

    input_data = run_info.input.read_text().splitlines(keepends=False)

    try:
        process_line = getattr(module, "process_line", None)
        if process_line:
            input_data = [process_line(line) for line in input_data]

        process_data = getattr(module, "process_data", None)
        if process_data:
            input_data = process_data(input_data)

    except Exception as error:
        return get_error(error, "Error processing input file")

    try:
        solutions = iter(module.run(input_data))
    except Exception as error:
        return get_error(error, "run() function needs to be a generator")

    try:
        first = next(solutions, None)
        return (
            first if run_info.parts & 0b01 else None,
            next(solutions, None) if run_info.parts & 0b10 else None,
        )
    except Exception as error:
        return get_error(error, "Error while calculating solution")
