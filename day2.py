#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import enum
import sys
from typing import Any, IO, Iterable, Iterator


class Direction(enum.Enum):
    """Enumeration of movement directions."""

    FORWARD = "forward"
    DOWN = "down"
    UP = "up"


@dataclasses.dataclass
class Position:
    """Represents a position in space."""

    x: int
    y: int

    def __add__(self, other: Any) -> Position:
        """Given a position, add its coordinates to this position."""
        if not isinstance(other, Position):
            return NotImplemented
        else:
            return Position(self.x + other.x, self.y + other.y)


@dataclasses.dataclass
class Move:
    """Represents a move in a particular direction."""

    direction: Direction
    amount: int

    def offset(self) -> Position:
        """Return the change in position resulting from this movement."""
        if self.direction is Direction.FORWARD:
            return Position(self.amount, 0)
        elif self.direction is Direction.DOWN:
            return Position(0, self.amount)
        elif self.direction is Direction.UP:
            return Position(0, -self.amount)
        else:
            raise NotImplementedError


def _parse_moves(f: IO) -> Iterator[Move]:
    """Yield moves parsed from the given file."""
    for line in f:
        direction, amount = line.strip().split()
        yield Move(Direction(direction), int(amount))


def _eval_moves(start: Position, moves: Iterable[Move]) -> Position:
    """Return the new position after making the given moves."""
    return sum((move.offset() for move in moves), start=start)


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        moves = _parse_moves(f)
        position = _eval_moves(Position(0, 0), moves)
        print(position.x * position.y)


if __name__ == "__main__":
    main(sys.argv[1:])
