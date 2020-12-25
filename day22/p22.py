#!/usr/bin/env python
"""Rank 187 on part 1 but struggled to grok the rules in part 2"""

from copy import deepcopy
from collections import deque
import sys


def calculate_score(deck):
    score = 0
    i = 1
    while deck:
        score += deck.pop() * i
        i += 1
    return score


def p1(deck1, deck2):
    while deck1 and deck2:
        c1, c2 = deck1.popleft(), deck2.popleft()
        assert c1 != c2
        if c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)

    winner = deck1 if deck1 else deck2
    return calculate_score(winner)


def play_recursive_combat(p1, p2):
    cache = set()
    while p1 and p2:
        if (tuple(p1), tuple(p2)) in cache:
            return (1, p1)

        cache.add((tuple(p1), tuple(p2)))
        c1, c2 = p1.popleft(), p2.popleft()
        if len(p1) < c1 or len(p2) < c2:
            assert c1 != c2
            result = (1, p1) if c1 > c2 else (2, p2)
        else:
            result = play_recursive_combat(deque(list(p1)[:c1]), deque(list(p2)[:c2]))

        if result[0] == 1:
            p1.append(c1)
            p1.append(c2)
        elif result[0] == 2:
            p2.append(c2)
            p2.append(c1)

    return (1, p1) if p1 else (2, p2)


def p2(deck1, deck2):
    result = play_recursive_combat(deck1, deck2)

    winner = result[1]
    return calculate_score(winner)


def main():
    with open(sys.argv[1]) as fin:
        data = [i.strip() for i in fin]
        idx = data.index("Player 2:")
        deck1 = deque(map(int, data[1 : idx - 1]))
        deck2 = deque(map(int, data[idx + 1 :]))

    print("Part 1: {}".format(p1(deepcopy(deck1), deepcopy(deck2))))
    print("Part 2: {}".format(p2(deepcopy(deck1), deepcopy(deck2))))


if __name__ == "__main__":
    main()
