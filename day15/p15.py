#!/usr/bin/env python
"""The naive brute-force solution from part 1 just worked™ on part 2, even though I didn't do
anything clever. The hardest part of this was reading. The website's rendering and narrow layout is
hard to read when the hours get late.
"""

from itertools import count
import sys


# Not sure why but I referred to the stated numbers as "guesses"
def solve(data, n):
    nums = [int(i) for i in data.split(",")]

    # Don't actually need to store all the guesses but it worked
    guesses = nums[:]
    # Map guess to a list of turn numbers where the end of the list contains the most recent turn number
    cache = {v: [i + 1] for i, v in enumerate(nums)}

    for i in count(len(guesses) + 1):
        last_guess = guesses[-1]
        if len(cache[last_guess]) == 1:
            new_guess = 0
        else:
            new_guess = cache[last_guess][-1] - cache[last_guess][-2]

        if i == n:
            return new_guess

        guesses.append(new_guess)
        if new_guess in cache:
            cache[new_guess] += [i]
        else:
            cache[new_guess] = [i]


def main():
    with open(sys.argv[1]) as fin:
        data = fin.read()

    print("Part 1: {}".format(solve(data, 2020)))
    print("Part 2: {}".format(solve(data, 30000000)))


if __name__ == "__main__":
    main()
