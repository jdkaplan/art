# advance functions
def forward(direction: (int, int)) -> (int, int):
    return direction


def backward(direction: (int, int)) -> (int, int):
    dr, dc = direction
    return (-dr, -dc)


def right(direction: (int, int)) -> (int, int):
    dr, dc = direction
    return (dc, -dr)


def left(direction: (int, int)) -> (int, int):
    dr, dc = direction
    return (-dc, dr)


def north(direction: (int, int)) -> (int, int):
    return (-1, 0)


def south(direction: (int, int)) -> (int, int):
    return (1, 0)


def east(direction: (int, int)) -> (int, int):
    return (0, 1)


def west(direction: (int, int)) -> (int, int):
    return (0, -1)


ADV_MAP = {
    "f": forward,
    "b": backward,
    "r": right,
    "l": left,
    "n": north,
    "s": south,
    "e": east,
    "w": west,
}


class Palette:
    def __init__(self, palette: list[str]):
        self.chars = read_palette(palette)

    @classmethod
    def default(cls):
        return cls("TODO CHANGE ME")

    def __getitem__(self, key):
        return self.chars[key]

    def __contains__(self, key):
        return key in self.chars


def read_palette(spec_lines: list[str]) -> dict:
    palette = {}
    for spec_line in spec_lines:
        try:
            char, adv, repro, trans, spawn = spec_line.strip()[::2]
            spawn_dir = None if spawn == "#" else ADV_MAP[spawn.lower()]((0, 0))
            palette[char] = (
                ADV_MAP[adv.lower()],
                bool(int(repro)),
                trans,
                spawn_dir,
            )
        except Exception:
            raise Exception("ERR: Malformed Palette!")
    return palette
