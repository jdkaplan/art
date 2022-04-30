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


def stay(direction: (int, int)) -> (int, int):
    return (0, 0)


ADV_MAP = {
    "f": forward,
    "b": backward,
    "r": right,
    "l": left,
    "n": north,
    "s": south,
    "e": east,
    "w": west,
    "-": stay
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

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default


class PaletteError(Exception):
    pass


def parse_palette_line(spec_line: str):
    if len(spec_line) != 9:
        raise PaletteError(f"Palette line '{spec_line}' is wrong length")
    for i in [1,3,5,7]:
        if spec_line[i] != " ":
            raise PaletteError(f"Invalid character at position {i} in palette line '{spec_line}'")

    char, adv, repro, trans, spawn = spec_line.strip()[::2]

    if adv.lower() not in ADV_MAP:
        raise PaletteError(f"Invalid Advance character in palette line '{spec_line}'")
    adv = ADV_MAP[adv.lower()]

    if repro not in "01":
        raise PaletteError(f"Invalid Reproduce character in palette line '{spec_line}'")
    repro = bool(int(repro))

    if spawn.lower() not in "nsew-#":
        raise PaletteError(f"Invalid Spawn character in palette line '{spec_line}'")
    spawn = None if spawn == "#" else ADV_MAP[spawn.lower()]((0, 0))

    return (char, (adv, repro, trans, spawn))


def read_palette(spec_lines: list[str]) -> dict:
    return dict([parse_palette_line(spec_line.strip()) for spec_line in spec_lines if spec_line.strip()])
