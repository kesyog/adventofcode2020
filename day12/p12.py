#!/usr/bin/env python

import sys


def p1(lines):
    R_map = {"E": "S", "S": "W", "W": "N", "N": "E"}
    L_map = {v: i for i, v in R_map.items()}

    face = "E"
    x = 0
    y = 0
    for line in lines:
        d = line[0]
        num = int(line[1:])
        if d == "R":
            rot = num // 90
            for _ in range(rot):
                face = R_map[face]
            continue
        if d == "L":
            rot = num // 90
            for _ in range(rot):
                face = L_map[face]
            continue
        if d == "F":
            d = face
        if d == "N":
            y += num
        if d == "S":
            y -= num
        if d == "E":
            x += num
        if d == "W":
            x -= num

    return abs(x) + abs(y)


def p2(lines):
    ship = [0, 0]
    way = [10, 1]

    for line in lines:
        d = line[0]
        num = int(line[1:])
        if d == "R":
            rot = num // 90
            for _ in range(rot):
                way = [way[1], -way[0]]
            continue
        if d == "L":
            rot = num // 90
            for _ in range(rot):
                way = [-way[1], way[0]]
            continue
        if d == "F":
            ship[0] += num * way[0]
            ship[1] += num * way[1]
        if d == "N":
            way[1] += num
        if d == "S":
            way[1] -= num
        if d == "E":
            way[0] += num
        if d == "W":
            way[0] -= num

    return abs(ship[0]) + abs(ship[1])


def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
