#!/usr/bin/env python

from functools import reduce
import sys


def p1(data):
    count = 0
    for answers in data:
        # Post-cleanup. Used the same idea but a bit uglier.
        union = reduce(set.union, [set(i) for i in answers.split("\n")])
        count += len(union)
    return count


def p2(data):
    count = 0
    for answers in data:
        # Post-cleanup. Used the same idea but a bit uglier.
        intersection = reduce(set.intersection, [set(i) for i in answers.split("\n")])
        count += len(intersection)
    return count


def main():
    with open(sys.argv[1]) as fin:
        data = fin.read().strip().split("\n\n")

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
