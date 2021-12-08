#!/usr/bin/env python3

import dataclasses
import sys
from typing import Iterable, Iterator


Signal = frozenset[str]

# Mapping from digits to activated segments in a working display.
#
# Not actually used; just for posterity.
_DIGITS_TO_SEGMENTS = {
    num: frozenset(segments)
    for num, segments in [
        (0, "abcefg"),
        (1, "cf"),
        (2, "acdeg"),
        (3, "acdfg"),
        (4, "bcdf"),
        (5, "abdfg"),
        (6, "abdefg"),
        (7, "acf"),
        (8, "abcdefg"),
        (9, "abcdfg"),
    ]
}


@dataclasses.dataclass
class Display:
    """Represents a single (broken) display."""

    digits: frozenset[Signal]
    outputs: list[Signal]


def _decode_signals(signals: Iterable[Signal]) -> dict[Signal, int]:
    """Determine the mapping from signals to intended digits for a broken display."""
    decoded: dict[int, Signal] = {}
    remaining = set(signals)

    def record(digit: int, signal: Signal) -> None:
        decoded[digit] = signal
        remaining.remove(signal)

    # Determine everything that's unambiguous in isolation.
    for signal in set(remaining):
        if len(signal) == 2:
            record(1, signal)
        elif len(signal) == 4:
            record(4, signal)
        elif len(signal) == 3:
            record(7, signal)
        elif len(signal) == 7:
            record(8, signal)

    assert set(decoded) == {1, 4, 7, 8}

    # 4 & x has length 2 for x=2 only
    # 4 & x has length 4 for x=9 only
    for signal in set(remaining):
        check = decoded[4] & signal
        if len(check) == 2:
            record(2, signal)
        elif len(check) == 4:
            record(9, signal)

    assert set(decoded) == {1, 2, 4, 7, 8, 9}

    # x - 1 has length 3 for x=3 only
    # x - 1 has length 5 for x=6 only
    for signal in set(remaining):
        check = signal - decoded[1]
        if len(check) == 3:
            record(3, signal)
        elif len(check) == 5:
            record(6, signal)

    assert set(decoded) == {1, 2, 3, 4, 6, 7, 8, 9}

    # Only 0 and 5 remain.
    #   1 & 0 has length 2
    #   1 & 5 has length 1
    for signal in set(remaining):
        check = decoded[1] & signal
        if len(check) == 2:
            record(0, signal)
        elif len(check) == 1:
            record(5, signal)

    assert not remaining
    assert len(decoded) == 10
    return {signal: digit for digit, signal in decoded.items()}


def _decode_output(display: Display) -> list[int]:
    """Determine the intended output digits for a broken display."""
    signal_to_digits = _decode_signals(display.digits)
    return [signal_to_digits[signal] for signal in display.outputs]


def _digits_to_int(digits: Iterable[int]) -> int:
    """Given `(a, b, c)` return `abc`."""
    return int("".join((str(digit)) for digit in digits))


def _parse_input(lines: Iterable[str]) -> Iterator[Display]:
    """Parse display states and outputs from input lines."""
    for line in lines:
        line = line.strip()
        digits, outputs = line.split("|")
        yield Display(
            digits=frozenset(frozenset(digit) for digit in digits.strip().split()),
            outputs=[frozenset(output) for output in outputs.strip().split()],
        )


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        displays = _parse_input(f)
        outputs = [_decode_output(display) for display in displays]
        print(sum(1 for output in outputs for digit in output if digit in {1, 4, 7, 8}))
        print(sum(_digits_to_int(output) for output in outputs))


if __name__ == "__main__":
    main(sys.argv[1:])
