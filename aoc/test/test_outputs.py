#!/usr/bin/env python3

"""Basic verification that each solution produces correct output."""

import importlib
from typing import Any

import pytest


@pytest.mark.parametrize(
    "n,pt1,pt2",
    [
        (1, "", "1516"),
        (2, "", "1488311643"),
        (3, "2954600", "1662846"),
        (4, "39902", "26936"),
        (5, "6113", "20373"),
        (6, "359344", "1629570219571"),
        (7, "349357", "96708205"),
        (8, "352", "936117"),
        (9, "478", "1327014"),
        (10, "462693", "3094671161"),
        (11, "1665", "235"),
        (12, "5076", "145643"),
        (
            13,
            "701",
            "\n".join(
                [
                    "#### ###  #### #  # ###  ####   ## #   ",
                    "#    #  # #    # #  #  # #       # #   ",
                    "###  #  # ###  ##   ###  ###     # #   ",
                    "#    ###  #    # #  #  # #       # #   ",
                    "#    #    #    # #  #  # #    #  # #   ",
                    "#    #    #### #  # ###  ####  ##  ####",
                ]
            ),
        ),
        (14, "2703", "2984946368465"),
    ],
)
def test_day_n(capsys: Any, n: int, pt1: str, pt2: str) -> None:
    dayn = importlib.import_module(f".day{n}", package="aoc")
    dayn.main([f"inputs/day{n}.txt"])  # type: ignore
    if not pt1:
        assert capsys.readouterr().out == f"{pt2}\n"
    else:
        assert capsys.readouterr().out == f"{pt1}\n{pt2}\n"
