#!/usr/bin/env python

import sys
import click

INITIAL_SEQ = "167248359"

## Part 1

def p1(initial_seq):
    circle = [int(i) for i in initial_seq]

    for _ in range(100):
        circle, removed = circle[0:1] + circle[4:], circle[1:4]
        destination = circle[0] - 1
        while destination not in circle:
            destination -= 1
            if destination <= 0:
                destination = max(circle)
                break
        ins_idx = circle.index(destination)
        circle = circle[:ins_idx + 1] + removed + circle[ins_idx + 1:]
        circle = circle[1:] + circle[0:1]

    one_idx = circle.index(1)
    return ''.join(map(str, circle[one_idx + 1:] + circle[:one_idx]))


def main():
    print("Part 1: {}".format(p1(INITIAL_SEQ)))


if __name__ == "__main__":
    main()
