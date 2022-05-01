import enum


class Brush:
    def __init__(self, r, c, direction):
        self.r = r
        self.c = c
        self.direction = direction

    def advance(self, advance_fn):
        self.direction = advance_fn(self.direction)

    def move(self, row_count, col_count):
        self.r += self.direction[0]
        self.c += self.direction[1]

        if self.r >= row_count:
            self.r = 0
        elif self.r < 0:
            self.r = row_count - 1

        if self.c >= col_count:
            self.c = 0
        elif self.c < 0:
            self.c = col_count - 1

    def __hash__(self):
        return hash((self.r, self.c, self.direction))

    def __eq__(self, other):
        return (self.r, self.c, self.direction) == (other.r, other.c, other.direction)

    def __repr__(self):
        return f"Brush({self.r}, {self.c}, {self.direction})"


class Simulator:
    def __init__(self, grid, language, *, brush_style="bold"):
        stability_index = 4
        brush_index = 3

        self.brushes = set()
        fake_lang = (None, None, None, None, 1)
        self.grid = [
            [(language.get(col, fake_lang)[stability_index], col) for col in row]
            for row in grid.splitlines()
        ]
        self.row_count = len(self.grid)
        self.col_count = max(len(row) for row in self.grid)
        self.language = language
        for r in range(self.row_count):
            for c in range(self.col_count):
                char = self.grid[r][c][1]
                if char not in self.language:
                    continue

                brush = self.language[char][brush_index]
                if brush is not None:
                    self.add_brush(Brush(r, c, brush))

        self.brush_style = brush_style

    def add_brush(self, brush):
        self.brushes.add(brush)

    def simulate(self):
        """Returns whether this was the last step of the simulation."""

        locs = set()
        brushes = list(self.brushes)
        self.brushes.clear()
        for brush in brushes:
            if self.grid[brush.r][brush.c][1] in self.language:
                (advance_fn, reproduce, _, _, _) = self.language[
                    self.grid[brush.r][brush.c][1]
                ]
                if reproduce:
                    locs.add((brush.r, brush.c))
                    self.brushes.add(brush)
                    brush = Brush(brush.r, brush.c, brush.direction)

                brush.advance(advance_fn)
                locs.add((brush.r, brush.c))
                if brush.direction is not None:
                    brush.move(self.row_count, self.col_count)
                    self.brushes.add(brush)

        for r, c in locs:
            stability, current = self.grid[r][c]
            if stability == 1:
                (_, _, next_char, _, _) = self.language[current]
                stability_index = 4
                if next_char in self.language:
                    transform = (self.language[next_char][stability_index], next_char)
                else:
                    transform = (1, next_char)
            else:
                transform = (stability - 1, current)
            self.grid[r][c] = transform

        return len(self.brushes) != 0

    def get_grid(self):
        return self.grid

    def __str__(self):
        string = ""
        brushes = set((brush.r, brush.c) for brush in self.brushes)
        for row in range(self.row_count):
            for col in range(self.col_count):
                is_brush = (row, col) in brushes
                if is_brush:
                    string += self._format_brush(self.grid[row][col][1])
                else:
                    string += self.grid[row][col][1]
            string += "\n"
        return string

    def _format_brush(self, char):
        style = self.brush_style
        if style == "bold":
            return "\033[1m" + char + "\033[0m"
        if style == "inverse":
            return "\033[7m" + char + "\033[m"
        return char
