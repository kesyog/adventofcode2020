#!/usr/bin/env python
"""I thought to overwrite the + and * operators but didn't spend the time looking up if it was
possible. Instead I wrote very janky, hard-to-debug parsing code."""

from operator import add, mul
import re
import sys

# Matches on expressions enclosed by a parentheses that do not contain parentheses
PAREN_REGEX = re.compile(r'\([\s\d*+]+\)')

## Part 1

# Evaluate an expression from left to right. Inputs should not have parentheses
def eval_exp(s):
     exp = s.strip().strip('()').split(' ')
     ans = int(exp[0])
     op = None
     for i in exp[1:]:
         if i == '+':
             op = add
         elif i == '*':
             op = mul
         else:
             i = int(i)
             ans = op(ans, i)
     return ans

assert(eval_exp('1 + 2 * 3') == 9)


# Repeatedly evaluates expressions inside of parentheses using eval_exp until no more parentheses are left
def p1(lines):
    s = 0
    for line in lines:
        res = line
        while PAREN_REGEX.search(res) is not None:
            res = PAREN_REGEX.sub(lambda m: str(eval_exp(m.group(0))), res)
        res = eval_exp(res.strip())
        s += res

    return s




## Part 2

def eval_exp2(s):
    # Reduce until complete
    while True:
        # Handle all simple summations first
        s = re.sub(r'\d+ \+ \d+', lambda m: str(eval(m.group(0))), s)
        # Handle a couple of edge cases where we're left with some expression without addition 
        s = re.sub(r'\([\d\*\s]+\)', lambda m: str(eval(m.group(0))), s)
        s = re.sub(r'^[\d\*\s]+$', lambda m: str(eval(m.group(0))), s)

        if re.match(r'^\d+$', s) is not None:
            return eval(s)

def p2(lines):
    s = 0
    for line in lines:
        res = line
        while PAREN_REGEX.search(res) is not None:
            res = PAREN_REGEX.sub(lambda m: str(eval_exp2(m.group(0))), res)
        res = eval_exp2(res.strip())
        s += res
    return s



def main():
    with open(sys.argv[1]) as fin:
        data = fin.readlines()

    print("Part 1: {}".format(p1(data)))
    print("Part 2: {}".format(p2(data)))


if __name__ == "__main__":
    main()
