#!/usr/bin/env python

import sys

# Find pair of numbers in `items` that add up to `target_sum`
def find_pair(items, target_sum):
    # Iterate through items, caching the number needed to sum to target_sum, while checking to see
    # if the item is already in the cache
    cache = set()
    for i in items:
        if i in cache:
            return i, target_sum - i
        else:
            cache.add(target_sum - i)
    return None


# Part 1
def part1(expenses):
    a, b = find_pair([int(i) for i in expenses], 2020)
    print("{} * {} = {}".format(a, b, a * b))
    return


# Part 2
def part2(expenses):
    for i in range(len(expenses) - 2):
        ret = find_pair(expenses[i + 1 :], 2020 - expenses[i])
        if ret is not None:
            a, b = ret
            print("{} * {} * {} = {}".format(expenses[i], a, b, a * b * expenses[i]))
            return


def main():
    # Sacrifice one pass through input file for readability
    with open(sys.argv[1]) as fin:
        expenses = [int(i) for i in fin]
    part1(expenses)
    part2(expenses)


if __name__ == "__main__":
    main()
