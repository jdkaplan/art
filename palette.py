from typing import Optional

# advance functions
def forward(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return direction


def backward(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    dr, dc = direction
    return (-dr, -dc)


def right(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    dr, dc = direction
    return (dc, -dr)


def left(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    dr, dc = direction
    return (-dc, dr)


def north(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (-1, 0)


def south(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (1, 0)


def east(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (0, 1)


def west(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (0, -1)


def northeast(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (-1, 1)


def northwest(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (-1, -1)


def southeast(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (1, 1)


def southwest(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (1, -1)


def stay(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return (0, 0)


def die(direction: Optional[tuple[int, int]]) -> Optional[tuple[int, int]]:
    return None


ADV_MAP = {
    "f": forward,
    "b": backward,
    "r": right,
    "l": left,
    "n": north,
    "s": south,
    "e": east,
    "w": west,
    "ne": northeast,
    "nw": northwest,
    "se": southeast,
    "sw": southwest,
    "-": stay,
    "x": die
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


def parse_character(spec_line: str, idx: int):
    return spec_line[idx], idx+1


def parse_advance(spec_line: str, idx: int):
    direction = spec_line[idx].lower()
    new_idx = idx + 1
    if spec_line[idx + 1] != " ":
        # digraph direction
        direction = spec_line[idx:idx+2].lower()
        new_idx = idx + 2

    if direction not in ADV_MAP:
        raise PaletteError(f"Invalid Advance specification in palette line '{spec_line}'")

    return ADV_MAP[direction], new_idx


def parse_reproduce(spec_line: str, idx: int):
    repro = spec_line[idx]
    if repro not in "01":
        raise PaletteError(f"Invalid Reproduce character in palette line '{spec_line}'")
    return bool(int(repro)), idx + 1


def parse_transform(spec_line: str, idx: int):
    stability = 1
    # this is tricky, we can have something like "50 ", with a space
    # character.  So we really need to look for the *next* token to handle
    # any weirdness
    space_idx = spec_line[idx + 1:].index(" ") + idx + 1
    if spec_line[space_idx + 1] == " ":
        # this means that the transform character is a space
        # or some other malformation
        space_idx += 1

    transform = spec_line[idx:space_idx]
    if len(transform) > 1:
        try:
            stability = int(transform[:-1])
            if stability < 1:
                raise PaletteError(
                    f"Nonpositive Stability factor in palette line '{spec_line}'"
                )
        except Exception:
            raise PaletteError(
                f"Invalid Stability factor in palette line '{spec_line}'"
            )
    transform = transform[-1]

    return (stability, transform), space_idx


def parse_spawn(spec_line: str, idx: int):
    spawn = spec_line[idx]
    spawn = spec_line[idx].lower()
    new_idx = idx + 1
    if idx + 1 < len(spec_line):
        # digraph direction
        spawn = spec_line[idx:idx+2].lower()
        new_idx = idx + 2
    if spawn not in {"n", "s", "e", "w", "ne", "nw", "se", "sw", "-", "#"}:
        raise PaletteError(f"Invalid Spawn character in palette line '{spec_line}'")
    spawn = None if spawn == "#" else ADV_MAP[spawn]((0, 0))
    return spawn, new_idx


def parse_palette_line(spec_line: str):
    def validate_space():
        if spec_line[new_idx] != " ":
            raise PaletteError(
                f"Invalid character at position {new_idx} in palette line '{spec_line}'"
            )
    try:
        char, new_idx = parse_character(spec_line, 0)
        validate_space()
        adv, new_idx = parse_advance(spec_line, new_idx + 1)
        validate_space()
        repro, new_idx = parse_reproduce(spec_line, new_idx + 1)
        validate_space()
        (stability, trans), new_idx = parse_transform(spec_line, new_idx + 1)
        validate_space()
        spawn, new_idx = parse_spawn(spec_line, new_idx + 1)
        if new_idx != len(spec_line):
            raise PaletteError(f"Unparsed characters in palette line '{spec_line}'")
    except PaletteError:
        raise
    except Exception:
        raise PaletteError(f"Unexpected error extracting fields from palette line '{spec_line}'")

    return (char, (adv, repro, trans, spawn, stability))


def read_palette(spec_lines: list[str]) -> dict:
    palette = {}
    for spec_line in spec_lines:
        line = spec_line.rstrip()
        if not line:
            continue

        char, spec = parse_palette_line(line)
        if char in palette:
            raise PaletteError(f"Duplicate palette key '{char}'")

        palette[char] = spec

    return palette
