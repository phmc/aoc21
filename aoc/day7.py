#!/usr/bin/env python3

import functools
import math
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
    # Minimum is within +/-0.5 of the mean of the positions.
    #
    # To see this, differentiate `sum((x - n)(x - n + 1)/2)` where n takes each
    # position over the sum.
    positions = list(positions)
    mean = sum(positions) / len(positions)
    # Need to check both to account for possible cumulative effect of 0.5
    # deviation plus rounding.
    lower, upper = math.floor(mean), math.ceil(mean)
    if _calculate_triangular_cost(lower, positions) < _calculate_triangular_cost(
        upper, positions
    ):
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
