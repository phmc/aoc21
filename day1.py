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


def _consecutive_elements(it: Iterator[T]) -> Iterator[tuple[T, T]]:
    """
    Yield consecutive elements from an iterator as `(current, previous)` pairs.

    The first pair consists of the second and first elements.

    """
    it, it_incr = itertools.tee(it, 2)
    try:
        next(it_incr, None)
    except StopIteration:
        return
    yield from zip(it_incr, it)


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        depths = _ints_from_stream(f)
        print(sum(int(curr > prev) for curr, prev in _consecutive_elements(depths)))


if __name__ == "__main__":
    main(sys.argv[1:])
