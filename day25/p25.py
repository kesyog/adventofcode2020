#!/usr/bin/env python
"""Not a particularly satisfying puzzle. Lots of instructions for what ended up being a simple problem."""

from itertools import product, repeat, count
import sys


def transform(n, loop_size):
    return pow(n, loop_size, 20201227)


def p1(n1, n2):
    for loop_size in count(1):
        ans = transform(7, loop_size)
        if ans == n1:
            return transform(n2, loop_size)


def main():
    with open(sys.argv[1]) as fin:
        data = [i.strip() for i in fin]
        n1, n2 = int(data[0]), int(data[1])

    print("Part 1: {}".format(p1(n1, n2)))


if __name__ == "__main__":
    main()
