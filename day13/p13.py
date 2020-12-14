#!/usr/bin/env python
"""Didn't see the smarter solution and ended up using a Chinese Remainder Theorem solver for Part 2. Not particularly satisfying."""

import sys


def p1(data):
    timestamp = int(data[0])
    busses = [int(i) for i in data[1].split(",") if i != "x"]
    wait_time = lambda bus: bus - (timestamp % bus)
    bus = min(busses, key=wait_time)
    return bus * wait_time(bus)


def p2(data):
    busses = [(i, int(bus)) for i, bus in enumerate(data[1].split(",")) if bus != "x"]

    # After getting stuck, I looked up how to solve systems of linear Diophantine equations, a still
    # unsolved mystery from Project Euler. Trying to solve by hand got nowhere but I found from
    # Wikipedia that this particular system could be solved using the Chinese Remainder Theorem
    # (CRT). Some rejiggering to get values to enter into an online CRT solver:
    return [((b - i) % b, b) for i, b in busses]


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(p1(data)))
    print("Part 2 (for CRT solver): {}".format(p2(data)))


if __name__ == "__main__":
    main()
