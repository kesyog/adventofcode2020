#!/usr/bin/env python
"""Cleaned up some variable names and added some comments but still a bit ugly

Naming conventions:
fields = numbers on a ticket
rules = field names
"""

from __future__ import print_function
import re
from collections import defaultdict
import sys


def main():
    # Refactored a bit to be able to use the original input file. In reality, I manually split the
    # input file into multiple files for ease of processing
    with open(sys.argv[1]) as fin:
        data = fin.read().strip()
        lines = data.split("\n")
        rules = [(int(i), int(j)) for i, j in re.findall(r"(\d+)-(\d+)", data)]

        tickets = lines[lines.index("nearby tickets:") + 1 :]
        # Find all numbers in the entire tickets file
        all_fields = list(map(int, re.findall(r"\d+", " ".join(tickets))))

        my_ticket = list(map(int, lines[lines.index("your ticket:") + 1].split(",")))

    ## Part 1

    count = 0
    for field in all_fields:
        for rmin, rmax in rules:
            if field >= rmin and field <= rmax:
                break
        else:
            count += field

    print("Part 1:", count)

    ## Part 2

    # Build list of good tickets
    good_tickets = []
    for ticket in tickets:
        ticket_fields = [int(i) for i in ticket.strip().split(",")]
        ticket_is_bad = False
        for field in ticket_fields:
            # Check if the field matches any rule
            for rmin, rmax in rules:
                if field >= rmin and field <= rmax:
                    break
            else:
                ticket_is_bad = True
                break
        if ticket_is_bad:
            continue
        good_tickets.append(ticket_fields)

    # Figure out which fields (by index) could match a given rule (by index). Rule indexes are 2x the
    # corresponding line number
    candidate_fields = defaultdict(list)
    for rule_idx in range(0, len(rules), 2):
        for field_idx in range(len(good_tickets[0])):
            for ticket in good_tickets:
                if not (
                    (
                        ticket[field_idx] >= rules[rule_idx][0]
                        and ticket[field_idx] <= rules[rule_idx][1]
                    )
                    or (
                        ticket[field_idx] >= rules[rule_idx + 1][0]
                        and ticket[field_idx] <= rules[rule_idx + 1][1]
                    )
                ):
                    break
            else:
                candidate_fields[rule_idx] += [field_idx]

    # Whittle down which field is which by process of elimination
    # If a given rule can only contain one field, remove that field as a possibility from all other rules
    # Rinse and repeat
    while max([len(i) for i in candidate_fields.values()]) > 1:
        set_rules = [k for k, v in candidate_fields.items() if len(v) == 1]
        for set_rule in set_rules:
            set_field = candidate_fields[set_rule][0]
            for other_field in candidate_fields:
                if (
                    other_field == set_rule
                    or set_field not in candidate_fields[other_field]
                ):
                    continue
                candidate_fields[other_field].remove(set_field)

    # Calculate solution for my ticket
    ans = 1
    # Departures are the first 6 rules
    for rule_idx in range(6):
        field_idx = candidate_fields[rule_idx * 2][0]
        ans *= my_ticket[field_idx]

    print("Part 2:", ans)


if __name__ == "__main__":
    main()
