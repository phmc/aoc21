#!/usr/bin/env python3

import collections
import itertools
import sys

from typing import Iterable, Iterator


Point = collections.namedtuple("Point", ["x", "y"])
Point.__doc__ = "Point in 2D space."


# Mapping from points to energy levels.
Energies = dict[Point, int]


def _get_neighbours(energies: Energies, point: Point) -> set[Point]:
    """Return neighbours of a point."""
    return {
        Point(x, y)
        for x, y in (
            (point.x + dx, point.y + dy)
            for dx, dy in itertools.product([-1, 0, 1], repeat=2)
            if dx or dy  # exclude the point itself
        )
        if (x, y) in energies
    }


def _get_flashers(energies: Energies) -> set[Point]:
    """Return all points due to flash."""
    return {point for point, energy in energies.items() if energy > 9}


def _step(start: Energies) -> tuple[int, Energies]:
    """
    Run a step of energy increase and flashing.

    Returns total number of flashes in the step, and the energy levels after
    the step.

    """
    energies = {point: energy + 1 for point, energy in start.items()}

    flashed: set[Point] = set()  # All points that have flashed in this step.
    flashers = _get_flashers(energies)  # All points due to flash next.
    while flashers:
        increases = collections.Counter(
            itertools.chain.from_iterable(
                _get_neighbours(energies, flasher) for flasher in flashers
            )
        )
        energies = {
            point: energy + increases[point] for point, energy in energies.items()
        }
        flashed.update(flashers)
        flashers = {point for point in _get_flashers(energies) if point not in flashed}

    energies.update({point: 0 for point in flashed})
    return len(flashed), energies


def _parse_input(lines: Iterable[str]) -> Energies:
    """Parse input lines into energy levels."""
    lines = (line.strip() for line in lines)
    return {
        Point(x, y): int(energy)
        for y, row in enumerate(lines)
        for x, energy in enumerate(row)
    }


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        energies = _parse_input(f)
        total_flashes = 0
        for _ in range(100):
            flashes, energies = _step(energies)
            total_flashes += flashes
        print(total_flashes)


if __name__ == "__main__":
    main(sys.argv[1:])
