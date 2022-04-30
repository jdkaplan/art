#!/usr/bin/python3
import sys
import os
import time

from palette import Palette
from simulator import Simulator


def main():
    args = sys.argv[1:]
    if len(args) > 1:
        with open(args.pop(0)) as pal:
            palette = Palette(pal.readlines())
    else:
        palette = Palette.default()

    with open(args.pop(0)) as art:
        sim = Simulator(art.read(), palette)

    print(sim)
    for _ in range(2):
        time.sleep(1)
        # os.system("clear")
        print("---------------------------")
        sim.simulate()
        print(sim)


main()
