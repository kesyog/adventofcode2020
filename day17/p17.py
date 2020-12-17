#!/usr/bin/env python
"""Straightforward changes from part 1 to part 2"""

from copy import deepcopy
from collections import defaultdict
from itertools import product
import sys

ACTIVE = "#"
INACTIVE = "."


def p1(data):
    dirs = list(product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]))
    dirs.remove((0, 0, 0))

    cache = defaultdict(lambda: INACTIVE)

    # Bounds of search space
    x_range = [0, len(data[0])]
    y_range = [0, len(data)]
    z_range = [0, 0]

    # Populate initial conditions
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            cache[(x, y, 0)] = c

    for _ in range(6):
        new_cache = deepcopy(cache)
        for x, y, z in product(
            range(x_range[0] - 1, x_range[1] + 2),
            range(y_range[0] - 1, y_range[1] + 2),
            range(z_range[0] - 1, z_range[1] + 2),
        ):
            n_active_neigh = 0
            for dx, dy, dz in dirs:
                if cache[(x + dx, y + dy, z + dz)] == ACTIVE:
                    n_active_neigh += 1
                    # No need to keep counting after 4
                    if n_active_neigh == 4:
                        break
            if cache[(x, y, z)] == ACTIVE and n_active_neigh not in (2, 3):
                new_cache[(x, y, z)] = INACTIVE
            elif cache[(x, y, z)] == INACTIVE and n_active_neigh == 3:
                new_cache[(x, y, z)] = ACTIVE
                x_range[0] = min(x, x_range[0])
                y_range[0] = min(y, y_range[0])
                z_range[0] = min(z, z_range[0])
                x_range[1] = max(x, x_range[1])
                y_range[1] = max(y, y_range[1])
                z_range[1] = max(z, z_range[1])
        cache = new_cache

    return len([i for i, v in cache.items() if v == ACTIVE])


def p2(data):
    dirs = list(product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]))
    dirs.remove((0, 0, 0, 0))

    cache = defaultdict(lambda: INACTIVE)

    # Bounds of search space
    w_range = [0, 0]
    x_range = [0, len(data[0])]
    y_range = [0, len(data)]
    z_range = [0, 0]

    # Populate initial conditions
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            cache[(0, x, y, 0)] = c

    for _ in range(6):
        new_cache = deepcopy(cache)
        for w, x, y, z in product(
            range(w_range[0] - 1, w_range[1] + 2),
            range(x_range[0] - 1, x_range[1] + 2),
            range(y_range[0] - 1, y_range[1] + 2),
            range(z_range[0] - 1, z_range[1] + 2),
        ):
            n_active_neigh = 0
            for dw, dx, dy, dz in dirs:
                if cache[(w + dw, x + dx, y + dy, z + dz)] == ACTIVE:
                    n_active_neigh += 1
                    # No need to keep counting after 4
                    if n_active_neigh == 4:
                        break
            if cache[(w, x, y, z)] == ACTIVE and n_active_neigh not in (2, 3):
                new_cache[(w, x, y, z)] = INACTIVE
            elif cache[(w, x, y, z)] == INACTIVE and n_active_neigh == 3:
                new_cache[(w, x, y, z)] = ACTIVE
                w_range[0] = min(w, w_range[0])
                x_range[0] = min(x, x_range[0])
                y_range[0] = min(y, y_range[0])
                z_range[0] = min(z, z_range[0])
                w_range[1] = max(w, w_range[1])
                x_range[1] = max(x, x_range[1])
                y_range[1] = max(y, y_range[1])
                z_range[1] = max(z, z_range[1])
        cache = new_cache

    return len([i for i, v in cache.items() if v == ACTIVE])


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
