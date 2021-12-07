#!/usr/bin/env python3

import sys
from typing import Iterable, Iterator


def _find_middle_position(positions: Iterable[int]) -> int:
    """Return the middle position among the given positions."""
    positions = sorted(positions)
    # In the case where there are an even number of starting positions, the
    # middle two positions have the same cost so arbitrarily choose the first.
    return positions[(len(positions) + 1) // 2]


def _parse_inputs(lines: Iterable[str]) -> Iterator[int]:
    """Parse starting positions from input lines."""
    for line in lines:
        if line := line.strip():
            yield from (int(tok) for tok in line.split(","))


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        starts = list(_parse_inputs(f))
        middle = _find_middle_position(starts)
        print(sum(abs(pos - middle) for pos in starts))


if __name__ == "__main__":
    main(sys.argv[1:])
