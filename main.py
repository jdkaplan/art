#!/usr/bin/python3
import argparse
import logging
import os
import sys
import time


from palette import Palette
from simulator import Simulator


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
    parser.add_argument(
        "-n",
        "--no-clear",
        action="store_true",
        default=False,
        help="Do not clear the screen between ticks (default: False)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbosity",
        action="count",
        default=0,
        help="Increase logging output",
    )
    parser.add_argument("art", type=str, help="The art to execute")

    return parser.parse_args()


def main(args):
    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=args.verbosity * 10,
    )

    if args.palette:
        with open(args.palette) as pal:
            palette = Palette(pal.readlines())
    else:
        try:
            dir_ = os.path.dirname(args.art)
            base, ext = os.path.splitext(os.path.basename(args.art))
            path = os.path.join(dir_, base + ".palette")
            with open(path) as pal:
                palette = Palette(pal.readlines())
        except OSError as e:
            logging.info(
                f"Did not find companion palette file at {path}. Using default palette."
            )
            palette = Palette.default()

    with open(args.art) as art:
        canvas = Simulator(art.read(), palette)

    while True:
        if args.no_clear:
            print()
        else:
            os.system("clear")

        print(canvas, end="")

        if not canvas.simulate():
            break

        if args.wait:
            input()
        else:
            time.sleep(args.tick)


if __name__ == "__main__":
    args = parse_args()
    main(args)
