#!/usr/bin/env python
"""Reworked solution with some cleanup ideas stolen from others"""

from copy import deepcopy
from itertools import product, count
import sys

OPEN = "L"
TAKEN = "#"
FLOOR = "."

DIRS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def run_simulation(board, run_round):
    board = deepcopy(board)
    while True:
        n_changes = run_round(board)
        if not n_changes:
            return sum([row.count("#") for row in board])


def part1(board):
    n_rows = len(board)
    n_cols = len(board[0])

    def count_adjacent(i, j, board):
        min_row = max(i - 1, 0)
        max_row = min(i + 1, n_rows - 1)
        max_col = min(j + 1, n_cols - 1)
        min_col = max(j - 1, 0)

        n = 0
        for seats in board[min_row : max_row + 1]:
            n += seats[min_col : max_col + 1].count("#")

        if board[i][j] == "#":
            n -= 1
        return n

    def run_round(board):
        changes = {}
        for i, j in product(range(n_rows), range(n_cols)):
            if board[i][j] == OPEN and count_adjacent(i, j, board) == 0:
                changes[(i, j)] = TAKEN
            elif board[i][j] == TAKEN and count_adjacent(i, j, board) >= 4:
                changes[(i, j)] = OPEN

        for (i, j), v in changes.items():
            board[i][j] = v

        return len(changes)

    return run_simulation(board, run_round)


# Runs in ~1 second. Not sure how to speed up further without parallelizing or rewriting in something faster
def part2(board):
    n_rows = len(board)
    n_cols = len(board[0])

    def count_visible(i, j, lines, shortcircuit=False):
        n = 0
        for dx, dy in DIRS:
            row, col = i, j
            while True:
                row += dx
                col += dy
                if row >= n_rows or col >= n_cols or row < 0 or col < 0:
                    break
                if lines[row][col] == TAKEN:
                    if shortcircuit:
                        return 1
                    n += 1
                    if n == 5:
                        return 5
                    break
                elif lines[row][col] == OPEN:
                    break
        return n

    def run_round(board):
        changes = {}
        for i, j in product(range(n_rows), range(n_cols)):
            if board[i][j] == OPEN and count_visible(i, j, board, True) == 0:
                changes[(i, j)] = TAKEN
            elif board[i][j] == TAKEN and count_visible(i, j, board) >= 5:
                changes[(i, j)] = OPEN

        for (i, j), v in changes.items():
            board[i][j] = v

        return len(changes)

    return run_simulation(board, run_round)


def main():
    with open(sys.argv[1]) as fin:
        board = [list(line) for line in fin]

    print("Part 1: {}".format(part1(board)))
    print("Part 2: {}".format(part2(board)))


if __name__ == "__main__":
    main()
