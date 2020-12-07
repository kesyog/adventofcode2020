#!/usr/bin/env python
"""
Terrible naming. Terrible code. Lost a lot of time losing track of my recursion and not testing
against the sample data.
"""

import re
import sys

## Part 1 helper functions

# Find parents
def parents(data, color):
    ans = []
    for i in data:
        res = re.search("(.+) bags contain.*" + color, i)
        if res is not None:
            ans.append(res.group(1))
    return ans


# Recurse up through parents
# cache is a set of all colors encountered
def recurse_parents(data, color, cache):
    if color in cache:
        return cache
    for i in parents(data, color):
        recurse_parents(data, i, cache)
        cache.add(i)
    return cache


# Takes a few seconds to run
def p1(data):
    cache = set()
    return len(recurse_parents(data, "shiny gold", cache))


## Part 2 helper functions

# Find children
def children(data, color):
    for i in data:
        res = re.search(color + ".+ contain (.*)", i)
        if res is None:
            continue
        res = re.findall(r"(\d+) (.+?) bag", res.group(1))
        return res


# Recurse through children
# cache is a dict mapping a color to the number of bags it contains
def recurse_children(data, color, cache):
    if color in cache:
        return cache[color]
    total = 0
    children_list = children(data, color)
    if not children_list:
        return 0
    for child in children_list:
        n, child_color = child
        n = int(n)
        result = recurse_children(data, child_color, cache)
        total += n * (result + 1)
        cache[child_color] = result
    return total


def p2(data):
    cache = {}
    return recurse_children(data, "shiny gold", cache)


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
