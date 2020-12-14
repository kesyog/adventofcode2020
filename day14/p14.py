#!/usr/bin/env python
"""Pretty happy the get_all_masks generator worked with just some minimal debugging"""

import re
import sys


def p1_store(reg, value, mask, cache):
    value = int(value)
    for i, bit in enumerate(reversed(mask)):
        if bit == "X":
            continue
        bit = int(bit)
        value &= ~(1 << i)
        value |= bit << i
    cache[int(reg)] = value


def p1(lines):
    cache = {}

    mask = "X"
    for line in lines:
        if "mask" in line:
            mask = re.search("= (\w+)", line).group(1)
        elif "mem" in line:
            res = re.search(r"\[(\d+)] = (\d+)", line)
            p1_store(res.group(1), res.group(2), mask, cache)

    return sum([v for i, v in cache.items()])




## Part 2
def get_all_masks(mask):
    if "X" in mask:
        i = mask.index("X")
        # c = clear bit
        mask = mask[:i] + "c" + mask[i + 1 :]
        for j in get_all_masks(mask):
            yield j
        mask = mask[:i] + "1" + mask[i + 1 :]
        for j in get_all_masks(mask):
            yield j
    else:
        yield mask


def p2_store(reg, value, mask_base, cache):
    base_reg = int(reg)
    for mask in get_all_masks(mask_base):
        reg = base_reg
        for i, bit in enumerate(reversed(mask)):
            assert bit != "X"
            if bit == "c":
                reg &= ~(1 << i)
            else:
                bit = int(bit)
                reg |= bit << i
        cache[reg] = int(value)


def p2(lines):
    cache = {}

    mask = "X"
    for line in lines:
        if "mask" in line:
            mask = re.search("= (\w+)", line).group(1)
        elif "mem" in line:
            res = re.search(r"\[(\d+)] = (\d+)", line)
            p2_store(res.group(1), res.group(2), mask, cache)

    return sum([v for i, v in cache.items()])


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
