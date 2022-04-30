import sys
import os
import time


class Palette:
    def __init__(self, palette: str):
        self.chars = {}
        # TODO
        pass

    @classmethod
    def default(cls):
        # TODO
        pass


class Canvas:
    def __init__(
        self,
        palette: Palette,
        art: str,
    ):
        self.palette = palette
        self.grid = [[char for char in line] for line in art.splitlines()]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)

    def tick(self):
        pass


def main():
    args = sys.argv[1:]
    if len(args) > 1:
        with open(args.pop(0)) as pal:
            palette = Palette(pal)
    else:
        palette = Palette.default()

    with open(args.pop(0)) as art:
        canvas = Canvas(palette, art.read())

    print(canvas)
    for _ in range(5):
        time.sleep(1)
        os.system("clear")
        canvas.tick()
        print(canvas)


main()
