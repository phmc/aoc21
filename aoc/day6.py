#!/usr/bin/env python3

import collections
import sys
from typing import Iterable, Iterator, Mapping


def _get_next_days_timers(today: collections.Counter[int]) -> collections.Counter[int]:
    """
    Return values for tomorrow's timers, based on today's timers.

    Input and output count the number of timers with each value.

    """
    tomorrow = collections.Counter(
        {value - 1: count for value, count in today.items() if value > 0}
    )
    expiring = today.get(0, 0)
    tomorrow.update({6: expiring, 8: expiring})
    return tomorrow


def _get_n_days_timers(
    today: collections.Counter[int], n: int
) -> collections.Counter[int]:
    """Return timer counts advanced n days."""
    counts = today
    for _ in range(n):
        counts = _get_next_days_timers(counts)
    return counts


def _parse_initial_timers(lines: Iterable[str]) -> Iterator[int]:
    """Yield timer values, parsed from input lines."""
    for line in lines:
        if line := line.strip():
            yield from (int(tok) for tok in line.split(","))


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        counts = collections.Counter(_parse_initial_timers(f))
        counts = _get_n_days_timers(counts, n=80)
        print(sum(counts.values()))
        counts = _get_n_days_timers(counts, n=(256 - 80))
        print(sum(counts.values()))


if __name__ == "__main__":
    main(sys.argv[1:])
