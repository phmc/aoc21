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
class Move:
    """Represents a move in a particular direction."""

    direction: Direction
    amount: int


@dataclasses.dataclass
class Position:
    """Represents a position in space."""

    x: int
    y: int
    aim: int

    def moved(self, move: Move) -> Position:
        """Return a new position, moving from the current position."""
        if move.direction is Direction.FORWARD:
            return dataclasses.replace(
                self, x=self.x + move.amount, y=self.y + move.amount * self.aim
            )
        elif move.direction is Direction.DOWN:
            return dataclasses.replace(self, aim=self.aim + move.amount)
        elif move.direction is Direction.UP:
            return dataclasses.replace(self, aim=self.aim - move.amount)
        else:
            raise NotImplementedError


def _parse_moves(f: IO) -> Iterator[Move]:
    """Yield moves parsed from the given file."""
    for line in f:
        direction, amount = line.strip().split()
        yield Move(Direction(direction), int(amount))


def _eval_moves(start: Position, moves: Iterable[Move]) -> Position:
    """Return the new position after making the given moves."""
    position = start
    for move in moves:
        position = position.moved(move)
    return position


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        moves = _parse_moves(f)
        position = _eval_moves(Position(0, 0, 0), moves)
        print(position.x * position.y)


if __name__ == "__main__":
    main(sys.argv[1:])
