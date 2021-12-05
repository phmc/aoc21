#!/usr/bin/env python3

import itertools
import sys
import typing
from typing import IO, Iterator


def _ints_from_stream(f: IO[str]) -> Iterator[int]:
    """
    Read lines from the given (open) file, as integers.

    Stops on the first non-integer.

    """
    for line in f:
        try:
            yield int(line.strip())
        except ValueError:
            return


T = typing.TypeVar("T")


def _consecutive_elements(src: Iterator[T], *, n) -> Iterator[tuple[T, ...]]:
    """
    Yield consecutive elements from an iterator as `n`-tuples.

    Elements are in earliest-to-latest order in each tuple.

    The first tuple consists of the first, second ... nth elements; the
    second consists of the second, third, ..., (n+1)th elements; and so on.

    """
    incr_its = itertools.tee(src, n)
    # Horrendous for large n. Don't care yet.
    for idx in range(1, n + 1):
        for it in incr_its[idx:]:
            try:
                next(it)
            except StopIteration:
                # Fewer than n elements in total.
                return
    yield from zip(*incr_its)


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        depths = _ints_from_stream(f)
        windows = _consecutive_elements(depths, n=3)
        sums = (sum(window) for window in windows)
        print(sum(int(curr > prev) for prev, curr in _consecutive_elements(sums, n=2)))


if __name__ == "__main__":
    main(sys.argv[1:])
