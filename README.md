# aoc-solutions
My Solutions to Advent of Code

## How to use
Put your input files into `input/<year>/<day>.txt` whereas `day` is padded to 2 places, so the input for day 1 for aoc 2021 would be `input/2021/01.txt`. You can use test files by appending a `#` to the name, like `input/2021/01#.txt`.

To run the solutions, you have to have Python installed. Use `python -m aoc pattern [pattern ...]` to output all the solutions that are implemented and match the pattern. The pattern is of the form `<year>-<day>-<part>` where each individual item can also be replaced with `*` to run all solutions.

To use the test input instead of the resular input, add `--test` to the commandline.

You can add `--language <language>` to run that specific languages solution implementation (default is to run the Python solutions).
