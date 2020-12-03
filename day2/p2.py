#!/usr/bin/env python

import re
import sys

PW_REGEX = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def part1(entries):
    n_good = 0
    for line in entries:
        match = PW_REGEX.search(line)
        assert match is not None

        lower, upper, char, password = match.groups()
        lower = int(lower)
        upper = int(upper)
        count = password.count(char)

        if lower <= count <= upper:
            n_good += 1
    return n_good


def part2(entries):
    n_good = 0
    for line in entries:
        match = PW_REGEX.search(line)
        assert match is not None

        lower, upper, char, password = match.groups()
        lower = int(lower)
        assert lower > 0
        upper = int(upper)
        assert upper > 0

        # Password is valid only if exactly one of the conditions is met
        if (password[lower - 1] == char) ^ (password[upper - 1] == char):
            n_good += 1
    return n_good


def main():
    with open(sys.argv[1]) as fin:
        data = [i.strip() for i in fin]

    print("Part 1: {}".format(part1(data)))
    print("Part 2: {}".format(part2(data)))


if __name__ == "__main__":
    main()
