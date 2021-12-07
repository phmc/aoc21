#!/usr/bin/env python3

import functools
import sys
from typing import Iterable, Iterator, Optional


def _calculate_linear_cost(target: int, positions: Iterable[int]) -> int:
    """Return the total cost of moving to the target position for a linear metric."""
    return sum(abs(pos - target) for pos in positions)


def _calculate_linear_optimum(positions: Iterable[int]) -> int:
    """Return the optimal position for a linear metric."""
    positions = sorted(positions)
    # It's the median!
    #
    # In the case where there are an even number of starting positions, the
    # middle two positions have the same cost so arbitrarily choose the first.
    return positions[(len(positions) + 1) // 2]


@functools.cache
def _triangular(n: int) -> int:
    """Return the nth triangular number."""
    return n * (n + 1) // 2


def _calculate_triangular_cost(target: int, positions: Iterable[int]) -> int:
    """Return the total cost of moving to the target position for a triangular metric."""
    return sum(_triangular(abs(pos - target)) for pos in positions)


def _calculate_triangular_optimum(positions: Iterable[int]) -> int:
    """Return the optimal position for a triangular metric."""
    # Assume that there is no local (but not global) minimum, and bisect.
    # Haven't proved this...
    positions = list(positions)
    lower = min(positions)
    lower_cost = _calculate_triangular_cost(lower, positions)
    upper = max(positions)
    upper_cost = _calculate_triangular_cost(upper, positions)

    while upper - lower > 1:
        if lower_cost <= upper_cost:
            # Selecting the lower half, so prefer a higher new upper bound.
            upper = (upper + lower + 1) // 2
            upper_cost = _calculate_triangular_cost(upper, positions)
        else:
            # Vice-versa, prefer a lower value.
            lower = (upper + lower) // 2
            lower_cost = _calculate_triangular_cost(lower, positions)

    if lower_cost < upper_cost:
        return lower
    else:
        return upper


def _parse_inputs(lines: Iterable[str]) -> Iterator[int]:
    """Parse starting positions from input lines."""
    for line in lines:
        if line := line.strip():
            yield from (int(tok) for tok in line.split(","))


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        starts = list(_parse_inputs(f))
        target = _calculate_linear_optimum(starts)
        print(_calculate_linear_cost(target, starts))
        target = _calculate_triangular_optimum(starts)
        print(_calculate_triangular_cost(target, starts))


if __name__ == "__main__":
    main(sys.argv[1:])
