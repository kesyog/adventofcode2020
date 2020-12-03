#!/usr/bin/env python

from operator import mul
from functools import reduce
from itertools import count
import sys


def check_slope(data, x_slope, y_slope, height, width):
    n_trees = 0
    for x_abs, y in zip(count(step=x_slope), range(0, height, y_slope)):
        x = x_abs % width
        if data[y][x] == "#":
            n_trees += 1
    return n_trees


def main():
    with open(sys.argv[1]) as fin:
        data = [i.strip() for i in fin]

    width = len(data[0])
    height = len(data)

    p1 = check_slope(data, 3, 1, height, width)
    p2 = reduce(
        mul,
        [
            check_slope(data, x, y, height, width)
            for (x, y) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        ],
    )

    print("Part 1: {}".format(p1))
    print("Part 2: {}".format(p2))


if __name__ == "__main__":
    main()
