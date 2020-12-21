#!/usr/bin/env python
"""Pretty straightforward. Painfully lost a lot of time learning the difference between '\W' and '\b' in regex syntax"""

import re
from collections import defaultdict
from functools import reduce
import sys


def p1(data):
    lines = data.split("\n")
    cache = defaultdict(list)
    all_ingredients = set()

    for line in lines:
        assert "contains" in line
        res = re.search(r"contains (.*)\)", line)
        allergens = res.group(1).split(", ")
        ingredients = line.split("(")[0].strip().split(" ")
        all_ingredients |= set(ingredients)
        for a in allergens:
            cache[a] += [set(ingredients)]

    unsafe = set()
    for _, items in cache.items():
        # Candidates appear in all rows for a given allergy
        candidates = reduce(set.intersection, items)
        unsafe |= candidates

    good_set = all_ingredients - unsafe
    return sum([len(re.findall(r"\b{}\b".format(i), data)) for i in good_set])


def p2(data):
    lines = data.split("\n")
    cache = defaultdict(list)
    all_ingredients = set()

    for line in lines:
        assert "contains" in line
        res = re.search(r"contains (.*)\)", line)
        allergens = res.group(1).split(", ")
        ingredients = line.split("(")[0].strip().split(" ")
        all_ingredients |= set(ingredients)
        for a in allergens:
            cache[a] += [set(ingredients)]

    unsafe = set()
    for allergen, items in cache.items():
        candidates = reduce(set.intersection, items)
        unsafe |= candidates
        cache[allergen] = candidates

    unsolved = set(cache.keys())
    solution = {}
    while unsolved:
        unique = [k for k in unsolved if len(cache[k]) == 1][0]
        solution[unique] = list(cache[unique])[0]
        for k in cache.keys():
            if k != unique:
                cache[k] -= cache[unique]
        unsolved.remove(unique)

    return ",".join([list(v)[0] for k, v in sorted(cache.items(), key=lambda a: a[0])])


def main():
    with open(sys.argv[1]) as fin:
        data = fin.read().strip()

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
