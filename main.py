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

    while True:
        os.system("clear")
        print(sim, end="")
        if not sim.simulate():
            break
        if len(args) != 0 and args.pop(0) == 'r':
            input()
        else:
            time.sleep(1)



main()
