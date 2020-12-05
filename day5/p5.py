#!/usr/bin/env python

import string
import sys


def p1(data):
    return max(data)


def p2(data):
    all_seats = set(range(min(data), max(data) + 1))
    unassigned_seats = all_seats - set(data)
    return unassigned_seats.pop()


def main():
    with open(sys.argv[1]) as fin:
        # Convert to binary string
        # RIP Python 3
        data = [line.translate(string.maketrans("FBLR", "0101")) for line in fin]
        # Convert to integer
        data = [int(i, 2) for i in data]

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
