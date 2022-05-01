#!/usr/bin/env python3

from sys import stdin

i = 0
for line in stdin:
    extra_offset = 4 if (i // (8 * 30)) % 2 == 1 else 0
    if (i - 2 - extra_offset) % (8 * 30) != 0:
        i += 1
        continue

    io = line.strip().replace("O", "0").replace("I", "|")
    print(io.replace("0", " ").replace("|", "█"))

    i += 1
