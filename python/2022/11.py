import operator
import re
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from heapq import nlargest

MONKEY_INFO_REGEX = re.compile(
    r"""Monkey \d+:
  Starting items: (?P<items>[\d, ]+)
  Operation: new = (?:(?P<a>\d+)|old) (?P<operator>[+\-*/]) (?:(?P<b>\d+)|old)
  Test: divisible by (?P<check>\d+)
    If true: throw to monkey (?P<result_true>\d+)
    If false: throw to monkey (?P<result_false>\d+)"""
)
OPERATOR_LOOKUP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def int_or_none(number):
    return number if number is None else int(number)


def process_data(data: list[str]):
    return [
        Monkey(
            int_or_none(monkey_info.group("a")),
            OPERATOR_LOOKUP[monkey_info.group("operator")],
            int_or_none(monkey_info.group("b")),
            int(monkey_info.group("check")),
            tuple(map(int, monkey_info.group("result_false", "result_true"))),
            MonkeyState(deque(map(int, monkey_info.group("items").split(", ")))),
        )
        for monkey_info in MONKEY_INFO_REGEX.finditer("\n".join(data))
    ]


@dataclass(slots=True)
class MonkeyState:
    items: deque[int]
    inspections: int
    _original_items: deque[int]

    def __init__(self, items):
        self.inspections: int = 0
        self._original_items = items

    def reset(self):
        self.items = self._original_items.copy()
        self.inspections = 0


@dataclass(slots=True, frozen=True)
class Monkey:
    a: int | None
    operation: Callable[[int, int], int]
    b: int | None
    check: int
    results: tuple[int, int]
    _state: MonkeyState

    @property
    def items(self):
        return self._state.items

    @property
    def inspections(self):
        return self._state.inspections

    def inspect(self) -> int:
        self._state.inspections += 1
        value = self._state.items.popleft()
        return self.operation(
            value if self.a is None else self.a,
            value if self.b is None else self.b,
        )

    def get_destination(self, result):
        return self.results[not (result % self.check)]

    def reset(self):
        self._state.reset()


def calculate(monkeys: list[Monkey], rounds: int, modulus: int, divisor=1):
    for monkey in monkeys:
        monkey.reset()

    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.inspect() % modulus // divisor
                destination = monkey.get_destination(item)
                monkeys[destination].items.append(item)

    return operator.mul(*nlargest(2, (monkey.inspections for monkey in monkeys)))


def run(monkeys: list[Monkey]):
    # Assumption: The mod check is always prime
    modulus = 1
    for monkey in monkeys:
        modulus *= monkey.check

    yield calculate(monkeys, 20, modulus, divisor=3)
    yield calculate(monkeys, 10_000, modulus)
