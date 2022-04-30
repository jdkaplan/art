# advance functions
def forward(direction: tuple[int, int]) -> tuple[int, int]:
    return direction


def backward(direction: tuple[int, int]) -> tuple[int, int]:
    dr, dc = direction
    return (-dr, -dc)


def right(direction: tuple[int, int]) -> tuple[int, int]:
    dr, dc = direction
    return (dc, -dr)


def left(direction: tuple[int, int]) -> tuple[int, int]:
    dr, dc = direction
    return (-dc, dr)


def north(direction: tuple[int, int]) -> tuple[int, int]:
    return (-1, 0)


def south(direction: tuple[int, int]) -> tuple[int, int]:
    return (1, 0)


def east(direction: tuple[int, int]) -> tuple[int, int]:
    return (0, 1)


def west(direction: tuple[int, int]) -> tuple[int, int]:
    return (0, -1)


def stay(direction: tuple[int, int]) -> tuple[int, int]:
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
    "-": stay,
}

_default_palette = """\
^ n 0 ^ n
v s 0 v s
> e 0 > e
< w 0 < w

. f 0 - #

r r 0 r #
l l 0 l #
f f 0 f #
b b 0 b #

n n 0 n #
s s 0 s #
e e 0 e #
w w 0 w #

R R 1 R #
L L 1 L #
F F 1 F #
B B 1 B #

N N 1 N #
S S 1 S #
E E 1 E #
W W 1 W #
"""


class Palette:
    def __init__(self, palette: list[str]):
        self.chars = read_palette(palette)

    @classmethod
    def default(cls):
        return cls(_default_palette.splitlines())

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
    for i in [1, 3, 5]:
        if spec_line[i] != " ":
            raise PaletteError(
                f"Invalid character at position {i} in palette line '{spec_line}'"
            )

    try:
        char = spec_line[0]
        adv = spec_line[2]
        repro = spec_line[4]
        trans = spec_line[6:-2]
        spawn = spec_line[-1]
    except Exception:
        raise PaletteError(f"Error extracting fields from pallete line '{spec_line}'")

    if adv.lower() not in ADV_MAP:
        raise PaletteError(f"Invalid Advance character in palette line '{spec_line}'")
    adv = ADV_MAP[adv.lower()]

    if repro not in "01":
        raise PaletteError(f"Invalid Reproduce character in palette line '{spec_line}'")
    repro = bool(int(repro))

    stability = 1
    if len(trans) > 1:
        try:
            stability = int(trans[:-1])
            if stability < 1:
                raise PaletteError(
                    f"Nonpositive Stability factor in palette line '{spec_line}'"
                )
        except Exception:
            raise PaletteError(
                f"Invalid Stability factor in palette line '{spec_line}'"
            )
    trans = trans[-1]

    if spawn.lower() not in "nsew-#":
        raise PaletteError(f"Invalid Spawn character in palette line '{spec_line}'")
    spawn = None if spawn == "#" else ADV_MAP[spawn.lower()]((0, 0))

    return (char, (adv, repro, trans, spawn, stability))


def read_palette(spec_lines: list[str]) -> dict:
    palette = {}
    for spec_line in spec_lines:
        line = spec_line.strip()
        if not line:
            continue

        char, spec = parse_palette_line(line)
        if char in palette:
            raise PaletteError(f"Duplicate palette key '{char}'")

        palette[char] = spec

    return palette
