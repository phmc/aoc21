#!/usr/bin/env python3

import collections
import itertools
import sys
from typing import IO, Iterable, Iterator, Sequence


def _enumerate_ones(binstr: str) -> set[int]:
    """Given a string of `1` and `0`, return the indices where `1` appears."""
    return {idx for idx, char in enumerate(binstr) if char == "1"}


def _calculate_gamma(diags: Sequence[str], diag_length: int) -> int:
    """Calculate the gamma value from diagnostic readings."""
    ones = collections.Counter(
        itertools.chain.from_iterable(_enumerate_ones(diag) for diag in diags)
    )
    threshold = len(diags) / 2
    gamma_chars = (
        "1" if ones.get(idx, 0) > threshold else "0" for idx in range(diag_length)
    )
    return int("".join(gamma_chars), 2)


def _calculate_epsilon(gamma: int, diag_length: int) -> int:
    """Calculate the epsilon value from the gamma value."""
    return gamma ^ ((2 ** diag_length) - 1)


def _get_diag_length(diags: Iterable[str]) -> int:
    """Return the (common) length of each diagnostic reading."""
    # Check while we're here...
    lengths = set(len(diag) for diag in diags)
    if len(lengths) != 1:
        raise ValueError(f"Multiple diags lengths: {lengths}")
    return next(iter(lengths))


def _parse_diags(f: IO[str]) -> Iterator[str]:
    """Parse diagnostic readings from a stream."""
    for line in f:
        if diag := line.strip():
            yield diag


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        diags = list(_parse_diags(f))
        diag_length = _get_diag_length(diags)
        gamma = _calculate_gamma(diags, diag_length)
        epsilon = _calculate_epsilon(gamma, diag_length)
        print(gamma * epsilon)


if __name__ == "__main__":
    main(sys.argv[1:])
