#!/usr/bin/env python

import re
import sys


def p1(passports):
    n_good = 0
    for passport in passports:
        # Super hacky check to see if all fields are present by simply counting fields
        n_fields = len(passport.split(" "))
        if n_fields == 8:
            n_good += 1
        elif n_fields == 7 and "cid" not in passport:
            n_good += 1
    return n_good


# Added some extra input validation while trying to diagnose a regex bug. Could use a lot more.
def p2(passports):
    n_good = 0
    for i in passports:
        field_db = {}
        # Add fields to field database
        for field in i.strip().split(" "):
            assert field[3] == ":"
            assert field[:3] not in field_db
            field_db[field[:3]] = field[4:]
        if len(field_db) < 7 or (len(field_db) == 7 and "cid" in field_db):
            continue
        if (
            len(field_db["byr"]) != 4
            or int(field_db["byr"]) < 1920
            or int(field_db["byr"]) > 2002
        ):
            continue
        if (
            len(field_db["eyr"]) != 4
            or int(field_db["eyr"]) < 2020
            or int(field_db["eyr"]) > 2030
        ):
            continue
        if (
            len(field_db["iyr"]) != 4
            or int(field_db["iyr"]) < 2010
            or int(field_db["iyr"]) > 2020
        ):
            continue
        if field_db["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            continue
        if re.match(r"^\d{9}$", field_db["pid"]) is None:
            continue
        if re.match(r"^#[a-fA-F0-9]{6}$", field_db["hcl"]) is None:
            continue
        height = re.match(r"^(\d+)(\w+)$", field_db["hgt"])
        if height is None:
            continue
        if height.group(2) == "cm":
            if int(height.group(1)) < 150 or int(height.group(1)) > 193:
                continue
        elif height.group(2) == "in":
            if int(height.group(1)) < 59 or int(height.group(1)) > 76:
                continue
        else:
            continue
        n_good += 1
    return n_good


def main():
    with open(sys.argv[1]) as fin:
        raw_data = fin.read().strip()

    # Passports are split by a blank line
    passports = raw_data.split("\n\n")
    # Convert multi-line passports to one line with all fields separated by one space
    passports = [re.sub(r"\n+", " ", i) for i in passports]

    print("Part 1: {}".format(p1(passports)))
    print("Part 2: {}".format(p2(passports)))


if __name__ == "__main__":
    main()
