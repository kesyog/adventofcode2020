#!/usr/bin/env python
"""Still bad at midnight recursion"""

from collections import Counter
import sys


def p1(numbers):
    numbers += [max(numbers) + 3]
    numbers = sorted(numbers)

    volt = 0
    diff = []
    for i in numbers:
        diff += [i - volt]
        volt = i

    counts = Counter(diff)
    return counts[1] * counts[3]


def n_combinations(start, finish, adapters, cache):
    if start == finish:
        return 1
    if start in cache:
        return cache[start]
    n = 0
    for adapter in [i for i in adapters if 1 <= (i - start) <= 3]:
        leftover_adapters = [i for i in adapters if i > adapter]
        res = n_combinations(adapter, finish, leftover_adapters, cache)
        cache[adapter] = res
        n += res
    return n


def p2(numbers):
    device = max(numbers)
    cache = {}
    return n_combinations(0, device, numbers, cache)


def main():
    with open(sys.argv[1]) as fin:
        numbers = [int(i) for i in fin]

    print("Part 1: {}".format(p1(numbers)))
    print("Part 2: {}".format(p2(numbers)))


if __name__ == "__main__":
    main()
