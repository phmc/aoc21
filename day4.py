#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import itertools
import sys
from typing import Iterable, Iterator, Sequence


@dataclasses.dataclass
class Board:
    """
    State of a board at some point in time.

    .. attribute:: rows

        Digits left unmarked in each row.

    .. attribute:: cols

        Digits left unmarked in each column.

    """

    rows: list[set[int]]
    cols: list[set[int]]

    @classmethod
    def from_input(cls, lines: Sequence[str]) -> Board:
        """Create a new board from lines of input representing initial state."""
        row_values = [[int(value) for value in line.split()] for line in lines]
        return Board(
            rows=[set(row) for row in row_values],
            cols=[set(col) for col in zip(*row_values)],
        )

    def mark(self, value: int) -> None:
        """Remove the given value from all row and columns."""
        for row, col in zip(self.rows, self.cols):
            row.discard(value)
            col.discard(value)

    def has_won(self) -> bool:
        """Return `True` if any row or column is empty."""
        return not all(itertools.chain(self.rows, self.cols))

    def score(self, final_call: int) -> int:
        """Calculate the score of this board."""
        return final_call * sum(itertools.chain.from_iterable(self.rows))


def _find_winner(calls: Iterable[int], boards: Sequence[Board]) -> tuple[Board, int]:
    """
    Return the first winning board and last called number for the given calls.

    This mutates the boards and returns the winning board in its final, marked
    state.

    """
    for call in calls:
        for board in boards:
            board.mark(call)
            if board.has_won():
                return board, call
    else:
        raise ValueError("Didn't find a winner")


def _parse_calls(lines: Iterator[str]) -> Iterator[int]:
    """Return called numbers, parsed from input lines."""
    calls = next(lines, "").strip()
    if following := next(lines, "").strip():
        raise ValueError(f"Expected a blank line after calls; got {following}")
    return (int(call) for call in calls.split(","))


def _parse_boards(lines: Iterator[str]) -> Iterator[Board]:
    """Return initial board states, parsed from input lines."""
    current_board: list[str] = []
    for line in lines:
        if not line.strip() and current_board:
            yield Board.from_input(current_board)
            current_board = []
        else:
            current_board.append(line)
    yield Board.from_input(current_board)


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        calls = _parse_calls(f)
        boards = _parse_boards(f)
        winner, final_call = _find_winner(calls, list(boards))
        print(winner.score(final_call))


if __name__ == "__main__":
    main(sys.argv[1:])
