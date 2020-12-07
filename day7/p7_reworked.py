#!/usr/bin/env python
"""
Initial solution was bad enough that I wanted to give it a second go without the time pressure.
Besides being a little more readable, it runs much faster now, since:
* The bag mapping is parsed and saved to a dict immediately
* In part 1, searching for all the bags that contain a given color takes longer than finding all the
colors within a given bag. Switching the direction of search made a huge difference.
"""

import re
import sys

## Part 1 helper functions

# Check whether the shiny gold bag is contained within the target colored bag
# cache is a dict storing whether a given colored bag contains the shiny gold bag
def is_shiny_gold_in_bag(mapping, color, cache):
    if color in cache:
        return cache[color]

    # No bags within
    if not mapping[color]:
        cache[color] = False
        return False

    for (n, child_color) in mapping[color]:
        if child_color == "shiny gold":
            cache[color] = True
            return True
        elif is_shiny_gold_in_bag(mapping, child_color, cache):
            cache[color] = True
            return True

    cache[color] = False
    return False


def p1(data):
    cache = {"shiny gold": False}
    return len([color for color in data if is_shiny_gold_in_bag(data, color, cache)])


## Part 2 helper functions

# Find number of bags contained within a given colored bag, not including the bag itself
# cache is a dict mapping a color to the number of bags it contains
def get_n_child_bags(mapping, color, cache):
    if color in cache:
        return cache[color]
    assert color in mapping

    # No bags within
    if not mapping[color]:
        return 0

    # Add up the number of child bags i.e. bags within the bag with the input color.
    # Include the number of bags within each child bag using a recursive search
    n_bags = 0
    for (n, child_color) in mapping[color]:
        n_child_bags = get_n_child_bags(mapping, child_color, cache)
        n_bags += n * (n_child_bags + 1)
        cache[child_color] = n_child_bags
    return n_bags


def p2(data):
    cache = {}
    return get_n_child_bags(data, "shiny gold", cache)


def main():
    with open(sys.argv[1]) as fin:
        # Parse input into a dict mapping each color to a list of (n, color) tuples indicating the contents of that bag
        mapping = {}
        for line in fin:
            res = re.search(r"(.+?)bag.+ contain (.*)", line)
            assert res is not None
            parent_bags = res.group(1).strip()
            child_bags = [
                (int(j), k) for (j, k) in re.findall(r"(\d+) (.+?) bag", res.group(2))
            ]
            mapping[parent_bags] = child_bags

    print("Part 1: {}".format(p1(mapping)))
    print("Part 2: {}".format(p2(mapping)))


if __name__ == "__main__":
    main()
