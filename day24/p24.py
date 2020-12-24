#!/usr/bin/env python
"""More or less a copy of the earlier Conway-type problem from this year"""

from copy import deepcopy
from collections import defaultdict
import sys

# Defined a coordinate system where these dx,dy pairs were adjacent tiles
ADJ = ((1, 0), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1))


def flip_tile(grid, d):
    x, y = 0, 0
    for direction in d:
        if direction == "e":
            x += 1
            continue
        if direction == "w":
            x -= 1
            continue
        if "n" in direction:
            y += 1
            if "w" in direction:
                x -= 1
        elif "s" in direction:
            y -= 1
            if "e" in direction:
                x += 1
    if grid[(x, y)] == True:
        del grid[(x, y)]
    else:
        grid[(x, y)] = True

    return grid


def p1(data):
    # init grid all white
    grid = defaultdict(lambda: False)

    for line in data:
        i = 0
        d = []
        while i < len(line):
            if line[i] in "we":
                d += [line[i : i + 1]]
                i += 1
            else:
                d += [line[i : i + 2]]
                i += 2
        grid = flip_tile(grid, d)

    # black = True
    n_black = len([i for i in grid.values() if i])
    return n_black, grid


def p2(data):
    grid = p1(data)[1]

    for _ in range(100):
        tiles_to_check = set()
        for (x, y) in grid.keys():
            tiles_to_check.add((x, y))
            for dx, dy in ADJ:
                tiles_to_check.add((x + dx, y + dy))
        new_grid = deepcopy(grid)
        for (x, y) in tiles_to_check:
            n_adjacent = 0
            for (dx, dy) in ADJ:
                if grid[(x + dx, y + dy)]:
                    n_adjacent += 1
                    if n_adjacent == 3:
                        break
            if grid[(x, y)] and n_adjacent != 1 and n_adjacent != 2:
                del new_grid[(x, y)]
            elif not grid[(x, y)] and n_adjacent == 2:
                new_grid[(x, y)] = True
        grid = new_grid
    return len([i for i in grid.values() if i])


def main():
    with open(sys.argv[1]) as fin:
        data = [i.strip() for i in fin]

    print("Part 1: {}".format(p1(data)[0]))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
