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
    'f': forward,
    'b': backward,
    'r': right,
    'l': left,
    'n': north,
    's': south,
    'e': east,
    'w': west
}

def read_pallet(fname: str) -> dict:
    pallet = {}
    with open(fname) as f:
        spec_lines = f.readlines()
        for spec_line in spec_lines:
            try:
                char, adv, repro, trans, spawn = spec_line.split(' ')
                spawn_dir = None if spawn == '#' else ADV_MAP[spawn]
                pallet[char] = (ADV_MAP[char.lower()], bool(repro), trans, spawn_dir)
            except Exception:
                raise Exception("ERR: Malformed Pallet!")
    return pallet
