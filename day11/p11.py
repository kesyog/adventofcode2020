#!/usr/bin/env python
"""Embarrassingly ugly, slow to run, slow to write, and full of indexing and bounds-checking footguns"""

import sys


def part1(lines):
    def count_adjacent(i, j, lines):
        min_row = max(i - 1, 0)
        max_row = min(i + 1, len(lines) - 1)
        max_col = min(j + 1, len(lines[0]) - 1)
        min_col = max(j - 1, 0)

        count = 0
        for seats in lines[min_row : max_row + 1]:
            count += seats[min_col : max_col + 1].count("#")

        if lines[i][j] == "#":
            count -= 1
        return count

    def run_round(lines):
        lines_new = lines[:]
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == "L" and count_adjacent(i, j, lines) == 0:
                    temp = list(lines_new[i])
                    temp[j] = "#"
                    lines_new[i] = "".join(temp)
                elif lines[i][j] == "#":
                    if count_adjacent(i, j, lines) >= 4:
                        temp = list(lines_new[i])
                        temp[j] = "L"
                        lines_new[i] = "".join(temp)
        return lines_new

    lines = lines[:]
    cache = set()
    while True:
        lines = run_round(lines)
        if str(lines) in cache:
            return sum([row.count("#") for row in lines])
        else:
            cache.add(str(lines))


# Takes a few (~5-10) seconds to run :(
def part2(lines):
    # Count visible seats
    def count_visible(i, j, lines):
        count = 0
        # Right
        if j != len(lines[0]) - 1:
            count += "#" in [x for x in lines[i][j + 1 :] if x != "."][:1]
        # Left
        if j != 0:
            try:
                count += "#" in [x for x in lines[i][:j] if x != "."][-1]
            except:
                pass
        # Down
        if i != len(lines) - 1:
            count += "#" in [z[j] for z in lines[i + 1 :] if z[j] != "."][:1]
        # Up
        if i != 0:
            try:
                count += "#" in [z[j] for z in lines[0:i] if z[j] != "."][-1]
            except:
                pass

        y = i - 1
        x1 = j + 1
        x2 = j - 1
        while y >= 0:
            if x1 is not None and x1 < len(lines[0]):
                if lines[y][x1] != ".":
                    count += lines[y][x1].count("#")
                    x1 = None
            if x2 is not None and x2 >= 0:
                if lines[y][x2] != ".":
                    count += lines[y][x2].count("#")
                    x2 = None
            y -= 1
            if x1 is not None:
                x1 += 1
            if x2 is not None:
                x2 -= 1

        y = i + 1
        x1 = j + 1
        x2 = j - 1
        while y < len(lines):
            if x1 is not None and x1 < len(lines[0]):
                if lines[y][x1] != ".":
                    count += lines[y][x1].count("#")
                    x1 = None
            if x2 is not None and x2 >= 0:
                if lines[y][x2] != ".":
                    count += lines[y][x2].count("#")
                    x2 = None
            y += 1
            if x1 is not None:
                x1 += 1
            if x2 is not None:
                x2 -= 1

        return count

    def run_round(lines):
        lines_new = lines[:]
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == "L" and count_visible(i, j, lines) == 0:
                    temp = list(lines_new[i])
                    temp[j] = "#"
                    lines_new[i] = "".join(temp)
                elif lines[i][j] == "#":
                    if count_visible(i, j, lines) >= 5:
                        temp = list(lines_new[i])
                        temp[j] = "L"
                        lines_new[i] = "".join(temp)
        return lines_new

    lines = lines[:]
    cache = set()
    while True:
        lines = run_round(lines)
        if str(lines) in cache:
            return sum([row.count("#") for row in lines])
        else:
            cache.add(str(lines))


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(part1(data)))
    print("Part 2: {}".format(part2(data)))


if __name__ == "__main__":
    main()
