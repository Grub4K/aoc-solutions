from __future__ import annotations

from aoc.run import RUNNERS
from aoc.run import execute


def get_args() -> tuple[str, list[str], bool]:
    import argparse

    parser = argparse.ArgumentParser(
        "aoc-runner",
        description="Generic runner for aoc-solutions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "pattern", nargs="+", help="pattern of solutions to execute (<year>-<day>-<part>)"
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="use input from the test file instead",
    )
    parser.add_argument(
        "-l",
        "--language",
        choices=RUNNERS,
        default="python",
        help="the language to run the selection in",
    )

    args = parser.parse_args()
    return args.language, args.pattern, args.test


def main():
    try:
        execute(*get_args())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
