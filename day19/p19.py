#!/usr/bin/env python
"""Wrote an ugly, slow parser that probably doesn't work for any general input. Spent a lot time debugging part 2."""

import re
import sys


def merge_into(bare_character_list, bare_key, other_list):  # -> list
    new_list = []
    for subrule in other_list:
        if re.search("\W" + bare_key + "\W", subrule) is None:
            new_list.append(subrule)
            continue

        for bare_rule in bare_character_list:
            new_list.append(
                re.sub("\W" + bare_key + "\W", " " + bare_rule + " ", subrule)
            )
    return list(set(new_list))


# Returns whether the given list of rules only contains raw strings
def contains_only_strings(rules_to_check):
    for i in rules_to_check:
        if re.search(r'^\W*"\w+"\W*$', i) is None:
            return False
    return True


# Return a dict of rules useful for later steps (0, 42, and 31) in the form:
# str(rule number): list of matching strings
def bubble_up_rules(rules):
    # Id's of rules that only contain strings
    simplified_rules = set()
    # Loop was super slow so I manually incremented this until the 0 rule was fully expanded
    for _ in range(17):
        for k in rules:
            # Bubble up any rules that only contain strings into rules that link to those rules
            if k not in simplified_rules and contains_only_strings(rules[k]):
                simplified_rules.add(k)
            if k in simplified_rules:
                for k2 in rules:
                    if k == k2 or k2 in simplified_rules:
                        continue
                    rules[k2] = merge_into(rules[k], k, rules[k2])
            else:
                for i in range(len(rules[k])):
                    # Concatenate adjacent strings into a single string
                    rules[k][i] = re.sub('"\s*"', "", rules[k][i])
                    # Clean up consecutive spaces
                    rules[k][i] = re.sub("\s+", " ", rules[k][i])

        # To speed up calculations, remove any rules that are no longer linked by any other rules
        # Make an exception for the rules that we'll need later
        present = set(
            re.findall("\d+", "".join([str(v) for v in rules.values()]))
        ) | set(["0", "42", "31"])
        all_keys = set(rules.keys())
        for k in all_keys - present:
            del rules[k]

    clean_rules = {}
    for k, v in sorted(rules.items(), key=lambda k: int(k[0])):
        clean_rules[k] = set([rule.strip(' "') for rule in rules[k]])

    return clean_rules


def p1(rules, input_data):
    count = 0
    for line in input_data:
        if line.strip() in rules["0"]:
            count += 1
    return count


def p2(rules, input_data):
    # Length of the strings that match 42
    block_len = len(list(rules["42"])[0])
    assert block_len == len(list(rules["31"])[0])

    # Any solution must match the following layout:
    # 1. Two matches of rule 42, one required by rule 8 and one required by rule 11
    # 2. (Optional) any number of matches of rule 42 (can come from 8 or 11). The number of 42's from 11
    # must match the number of 31's
    # 3. One match of rule 31
    # 4. (Optional) any number of matches of rule 31
    count = 0
    for line in input_data:
        line = line.strip()
        i = 0
        assert len(line) % block_len == 0
        not_match = False
        # Require two 42's
        for _ in range(2):
            assert len(line[i : i + block_len]) == block_len
            if line[i : i + block_len] not in rules["42"]:
                not_match = True
                break
            i += block_len
        if not_match:
            continue
        # Optional 42's
        n_42 = 2
        while (
            len(line[i : i + block_len]) == block_len
            and line[i : i + block_len] in rules["42"]
        ):
            n_42 += 1
            i += block_len
        # Required 31
        if line[i : i + block_len] not in rules["31"]:
            continue
        i += block_len
        n_31 = 1
        # Optional 31's
        while i < len(line):
            assert len(line[i : i + block_len]) == block_len
            if line[i : i + block_len] not in rules["31"]:
                not_match = True
                break
            n_31 += 1
            i += block_len
        # Every 11 adds a 42 so make sure we have enough 42's for the number of 11's we have
        if not_match or n_42 - 1 < n_31:
            continue
        count += 1

    return count


# Return rules as a dict: str(key): str(rule text)
def parse_input(data):
    lines = data.split("\n")
    rules_data = lines[: lines.index("")]
    input_data = lines[lines.index("") + 1 :]

    rules = {}
    for line in rules_data:
        pre, post = line.split(": ")
        rules[pre] = (" " + post + " ").split("|")

    return rules, input_data


def main():
    with open(sys.argv[1]) as fin:
        rules, input_data = parse_input(fin.read().strip())
        rules = bubble_up_rules(rules)

    print("Part 1: {}".format(p1(rules, input_data)))
    print("Part 2: {}".format(p2(rules, input_data)))


if __name__ == "__main__":
    main()
