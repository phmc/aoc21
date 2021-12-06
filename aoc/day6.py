#!/usr/bin/env python3

import sys
from typing import Iterable, Iterator


def _get_next_days_timers(timers: Iterable[int]) -> Iterator[int]:
    """Yield values for tomorrow's timers, based on today's timers."""
    for timer in timers:
        if not timer:
            yield 6
            yield 8
        else:
            assert timer > 0
            yield timer - 1


def _parse_initial_timers(lines: Iterable[str]) -> Iterator[int]:
    """Yield timer values, parsed from input lines."""
    for line in lines:
        if line := line.strip():
            yield from (int(tok) for tok in line.split(","))


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        timers = _parse_initial_timers(f)
        for _ in range(80):
            timers = _get_next_days_timers(timers)
        print(len(list(timers)))


if __name__ == "__main__":
    main(sys.argv[1:])
