#!/usr/bin/env python

import re
import sys

## Part 1


def part1(data):
    cache = set()
    a = 0
    i = 0
    while i not in cache:
        line = data[i]
        cache.add(i)
        op, num = line.split(" ")
        num = int(num)
        if op == "acc":
            a += num
            i += 1
        elif op == "jmp":
            i += num
        else:
            i += 1

    return a


## Part 2

# Return accumulator if successful or None otherwise
def is_winner(lines):
    cache = set()
    a = 0
    i = 0
    while i not in cache:
        line = lines[i]
        cache.add(i)
        op, num = line.split(" ")
        num = int(num)
        if op == "acc":
            a += num
            i += 1
        elif op == "jmp":
            i += num
        else:
            i += 1
        if i == len(lines):
            return a
    return None


def part2(data):
    # Save a copy
    og_data = data[:]

    # check all nops
    for i in range(len(data)):
        if "nop" in data[i]:
            data[i] = re.sub("nop", "jmp", data[i])
            result = is_winner(data)
            if result is not None:
                return result
            else:
                # Restore from copy
                data = og_data[:]

    # check all jmps
    for i in range(len(data)):
        if "jmp" in data[i]:
            data[i] = re.sub("jmp", "nop", data[i])
            result = is_winner(data)
            if result is not None:
                return result
            else:
                # Restore from copy
                data = og_data[:]


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(part1(data)))
    print("Part 2: {}".format(part2(data)))


if __name__ == "__main__":
    main()
