#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import enum
import sys
from typing import Iterable, Iterator


_VERSION_LEN = 3
_TYPE_ID_LEN = 3
_NIBBLE_HEAD_LEN = 1
_NIBBLE_LEN = 4
_OP_HEAD_LEN = 1
_OP_BIT_COUNT_LEN = 15
_OP_SUB_COUNT_LEN = 11


class PacketType(enum.Enum):
    """Enumeration of packet types."""

    OPERATOR = None
    LITERAL = 0b100

    @classmethod
    def from_id(cls, id: int) -> PacketType:
        """Return the packet type corresponding to a numeric ID."""
        try:
            return cls(id)
        except ValueError:
            return cls.OPERATOR


class OperatorLengthType(enum.Enum):
    """Enumeration of operator length types."""

    BIT_COUNT = 0
    SUB_COUNT = 1


@dataclasses.dataclass
class Packet:
    """Parsed packet."""

    version: int
    length: int


class _Parser:
    """Tracks parsing state for a single packet."""

    src: Iterator[str]
    bits_read: int = 0

    def __init__(self, src: Iterator[str]) -> None:
        self.src = src

    def __repr__(self) -> str:
        return f"{type(self).__name__}(bits_read={self.bits_read})"

    def parse(self) -> Iterator[Packet]:
        """Execute the parsing, yielding all sub-packets then the packet itself."""
        version = self._parse_version()
        pkt_type = self._parse_type()

        if pkt_type is PacketType.LITERAL:
            _ = self._parse_literal_body()

        elif pkt_type is PacketType.OPERATOR:
            yield from self._parse_sub_packets()

        else:
            raise NotImplementedError

        yield Packet(version, length=self.bits_read)

    # ---------------------------------------------------------------------------
    # Implementation details
    #

    def _read(self, n: int) -> str:
        """Read n characters and return as a string."""
        chars = []
        for _ in range(n):
            try:
                chars.append(next(self.src))
            except StopIteration:
                raise RuntimeError("Unexpected end of string")
        self.bits_read += n
        return "".join(chars)

    def _read_int(self, n: int) -> int:
        """Read n characters and return as an int."""
        return int(self._read(n), 2)

    def _parse_version(self) -> int:
        """Parse a packet version."""
        return self._read_int(_VERSION_LEN)

    def _parse_type(self) -> PacketType:
        """Parse a packet type."""
        return PacketType.from_id(self._read_int(_TYPE_ID_LEN))

    def _parse_literal_body(self) -> int:
        """Parse the contents of a literal packet."""
        nibbles: list[str] = []
        while True:
            more = self._read_int(_NIBBLE_HEAD_LEN)
            nibbles.append(self._read(_NIBBLE_LEN))
            if not more:
                break
        return int("".join(nibbles), 2)

    def _parse_sub_packet(self) -> Iterator[Packet]:
        """Helper to parse a single sub-packet."""
        yield from type(self)(self.src).parse()

    def _parse_sub_packets(self) -> Iterator[Packet]:
        """Parse sub-packets in an operator packet."""
        length_type = OperatorLengthType(self._read_int(_OP_HEAD_LEN))
        if length_type is OperatorLengthType.BIT_COUNT:
            bit_count = self._read_int(_OP_BIT_COUNT_LEN)
            bits_read = 0
            while bits_read < bit_count:
                for packet in self._parse_sub_packet():
                    bits_read += packet.length
                    yield packet
            if bits_read != bit_count:
                raise RuntimeError(
                    f"Expected to read {bit_count} bits, but only parsed {bits_read}"
                )

        elif length_type is OperatorLengthType.SUB_COUNT:
            sub_count = self._read_int(_OP_SUB_COUNT_LEN)
            for _ in range(sub_count):
                yield from self._parse_sub_packet()


def _hextobin(hexstr: Iterable[str]) -> Iterator[str]:
    """Given a hex string, yield corresponding binary string characters."""
    for char in hexstr:
        yield from f"{int(char, 16):04b}"


def main(argv: list[str]) -> None:
    with open(argv[0]) as f:
        binstr = _hextobin(f.read().strip())
        parser = _Parser(binstr)
        print(sum(pkt.version for pkt in parser.parse()))


if __name__ == "__main__":
    main(sys.argv[1:])
