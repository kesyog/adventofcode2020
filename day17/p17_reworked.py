#!/usr/bin/env python
"""Reworked to only keep track of active points to save space and only search active points and their neighbors to save time"""

from itertools import product
import sys

ACTIVE = "#"
INACTIVE = "."


def p1(data):
    dirs = list(product([-1, 0, 1], repeat=3))
    dirs.remove((0, 0, 0))

    # Set of x, y, z coordinate tuples of all active points
    active_points = set()

    # Populate initial conditions
    for y, line in enumerate(data):
        for x, c in enumerate(line.strip()):
            if c == ACTIVE:
                # Set z initial value to 0
                active_points.add((x, y, 0))

    for _turn in range(6):
        points_to_check = active_points.copy()
        for x, y, z in active_points:
            for dx, dy, dz in dirs:
                points_to_check.add((x + dx, y + dy, z + dz))

        new_active_points = active_points.copy()
        for x, y, z in points_to_check:
            # Count active neighbors
            n_active_neighbors = 0
            for dx, dy, dz in dirs:
                if (x + dx, y + dy, z + dz) in active_points:
                    n_active_neighbors += 1
                    # No need to keep counting past 4 based on the active<->inactive switching rules
                    if n_active_neighbors == 4:
                        break
            # Process switching rules
            if (x, y, z) in active_points:
                if n_active_neighbors not in (2, 3):
                    new_active_points.remove((x, y, z))
            elif (x, y, z) not in active_points and n_active_neighbors == 3:
                new_active_points.add((x, y, z))
        active_points = new_active_points

    return len(active_points)


def p2(data):
    dirs = list(product([-1, 0, 1], repeat=4))
    dirs.remove((0, 0, 0, 0))

    # Set of w, x, y, z coordinate tuples of all active points
    active_points = set()

    # Populate initial conditions
    for y, line in enumerate(data):
        for x, c in enumerate(line.strip()):
            if c == ACTIVE:
                # Set w and z initial values to 0
                active_points.add((0, x, y, 0))

    for _turn in range(6):
        points_to_check = active_points.copy()

        for w, x, y, z in active_points:
            for dw, dx, dy, dz in dirs:
                points_to_check.add((w + dw, x + dx, y + dy, z + dz))

        new_active_points = active_points.copy()
        for w, x, y, z in points_to_check:
            # Count active neighbors
            n_active_neighbors = 0
            for dw, dx, dy, dz in dirs:
                if (w + dw, x + dx, y + dy, z + dz) in active_points:
                    n_active_neighbors += 1
                    # No need to keep counting past 4 based on the active<->inactive switching rules
                    if n_active_neighbors == 4:
                        break
            # Process switching rules
            if (w, x, y, z) in active_points:
                if n_active_neighbors not in (2, 3):
                    new_active_points.remove((w, x, y, z))
            elif (w, x, y, z) not in active_points and n_active_neighbors == 3:
                new_active_points.add((w, x, y, z))
        active_points = new_active_points

    return len(active_points)


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
