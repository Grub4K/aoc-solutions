import importlib.machinery
import importlib.util
import sys
import traceback
from pathlib import Path

base_path = Path(__file__).parent


def get_args() -> tuple[str, bool]:
    import argparse

    parser = argparse.ArgumentParser(
        "py-aoc-runner",
        description="Python runner for aoc-solutions",
    )
    parser.add_argument("filter", help="a filter of solutions to execute")
    parser.add_argument(
        "--test", action="store_true", help="take input from the testfiles instead"
    )

    args = parser.parse_args()
    return args.filter, args.test


def import_file(file, name):
    loader = importlib.machinery.SourceFileLoader(name, str(file))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise ImportError(f"Could not construct spec for '{file}'")

    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    return mod


def run_python(year, day, test=False):
    python_path = base_path / "python"
    sys.path.insert(0, str(python_path))

    for day_path in python_path.glob(f"{year}/{day}.py"):
        year_path = day_path.parent.parent
        day_id = f"{year_path.stem}-{day_path.stem}"

        def print_error(message=None, stacklevel=0, limit=None):
            message = f"{message}: " if message else ""
            error = sys.exc_info()[1]
            assert error is not None

            exception = traceback.format_exception_only(error)[-1]  # type: ignore
            trimmed_summary = traceback.extract_tb(error.__traceback__, limit=limit)[
                stacklevel:
            ]
            tb = "".join(traceback.StackSummary.from_list(trimmed_summary).format())
            print(f"{day_id}: {message}{exception}{tb}")

        try:
            module = import_file(day_path, day_id)

        except Exception:
            # Assumption: importlib.import_module takes 3 function calls
            print_error("Error importing the module", 4)
            continue

        try:
            input_path = Path(
                "input", day_path.with_suffix(".txt").relative_to(python_path)
            )
            if test:  # Use input files with a `#` suffixed for debugging
                input_path = input_path.with_stem(f"{input_path.stem}#")
            input_data = input_path.read_text().splitlines(keepends=False)

            process_line = getattr(module, "process_line", None)
            if process_line:
                input_data = [process_line(line) for line in input_data]

            process_data = getattr(module, "process_data", None)
            if process_data:
                input_data = process_data(input_data)

        except FileNotFoundError:
            print_error("Error locating input file", limit=1)
            continue

        except Exception:
            print_error("Error processing input file")
            continue

        try:
            solutions = iter(module.run(input_data))

        except Exception:
            print_error("Error in run() function")
            continue

        try:
            for part in "ab":
                solution = next(solutions, None)
                if solution is not None:
                    print(f"{day_id} {part}: {solution}")

        except Exception:
            print_error("Error while calculating solution")


if __name__ == "__main__":
    data, test_mode = get_args()
    year, _, day = data.partition("-")
    day = day.zfill(2) if day else "*"

    run_python(year, day, test=test_mode)
