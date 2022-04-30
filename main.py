#!/usr/bin/python3
import argparse
import os
import sys
import time


from palette import Palette
from simulator import Simulator


# TODO(@jdkaplan): panic on palette failure


def parse_args():
    parser = argparse.ArgumentParser(
        description="ART: Advance Reproduce Transform",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-p",
        "--palette",
        type=str,
        help="The palette used to create the art (default: embedded default palette)",
    )
    parser.add_argument(
        "-t",
        "--tick",
        type=float,
        default=0.25,
        help="Tick delay in seconds (default: 0.25)",
    )
    parser.add_argument(
        "-w",
        "--wait",
        action="store_true",
        default=False,
        help="Wait for an Enter press before ticking",
    )
    parser.add_argument("art", type=str, help="The art to execute")

    return parser.parse_args()


def main(args):
    if args.palette:
        with open(args.palette) as pal:
            palette = Palette(pal.readlines())
    else:
        palette = Palette.default()

    with open(args.art) as art:
        sim = Simulator(art.read(), palette)

    while True:
        os.system("clear")
        print(sim, end="")

        if not sim.simulate():
            break

        if args.wait:
            input()
        else:
            time.sleep(args.tick)


if __name__ == "__main__":
    args = parse_args()
    main(args)
