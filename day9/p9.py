#!/usr/bin/env python
"""Problem statement reading failures on repeat"""

from collections import deque
import sys


def is_winner(num, rolling):
    cache = set(rolling)
    for i in rolling:
        if num - i in cache:
            return False
    return True


# pre = length of preamble for debugging
def part1(numbers, pre):
    rolling = deque(numbers[:pre])
    for i, v in enumerate(numbers):
        if i < pre:
            continue
        if is_winner(v, rolling):
            return v
        else:
            rolling.append(v)
            rolling.popleft()


def part2(numbers, target):
    for i, v in enumerate(numbers):
        tot = v
        nums = [v]
        for j in range(i + 1, len(numbers)):
            tot += numbers[j]
            nums.append(numbers[j])
            if tot == target:
                return v + max(nums)
            else:
                if tot > target:
                    break


def main():
    with open(sys.argv[1]) as fin:
        numbers = [int(i) for i in fin]

    p1_ans = part1(numbers, 25)
    print("Part 1: {}".format(p1_ans))
    print("Part 2: {}".format(part2(numbers, p1_ans)))


if __name__ == "__main__":
    main()
