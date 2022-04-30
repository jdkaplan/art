class Cursor:
    def __init__(self, r, c, direction):
        self.r = r
        self.c = c
        self.direction = direction

    def transform(self, transform_fn):
        self.direction = transform_fn(self.direction)

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


class Simulator:
    def __init__(self, grid, language):
        self.cursors = set()
        self.grid = [[col for col in row] for row in grid.splitlines()]
        self.row_count = len(self.grid)
        self.col_count = max(len(row) for row in self.grid)
        self.language = language
        cursor_index = 3
        for r in range(self.row_count):
            for c in range(self.col_count):
                char = self.grid[r][c]
                if char not in self.language:
                    continue

                cursor = self.language[char][cursor_index]
                if cursor is not None:
                    self.add_cursor(Cursor(r, c, cursor))

    def add_cursor(self, cursor):
        self.cursors.add(cursor)

    def simulate(self):
        """Returns whether this was the last step of the simulation."""

        locs = set()
        cursors = list(self.cursors)
        for cursor in cursors:
            self.cursors.remove(cursor)
            if self.grid[cursor.r][cursor.c] in self.language:
                (transform_fn, reproduce, _, _) = self.language[
                    self.grid[cursor.r][cursor.c]
                ]
                if reproduce:
                    locs.add((cursor.r, cursor.c))
                    cursor = Cursor(cursor.r, cursor.c, cursor.direction)
                cursor.transform(transform_fn)
                self.cursors.add(cursor)
                locs.add((cursor.r, cursor.c))

        for r, c in locs:
            (_, _, output, _) = self.language[self.grid[r][c]]
            self.grid[r][c] = output

        return len(self.cursors) != 0

    def get_grid(self):
        return self.grid

    def __str__(self):
        string = ""
        cursors = set((cursor.r, cursor.c) for cursor in self.cursors)
        for row in range(self.row_count):
            for col in range(self.col_count):
                is_cursor = (row, col) in cursors
                if is_cursor:
                    string += "\033[1m" + self.grid[row][col] + "\033[0m"
                else:
                    string += self.grid[row][col]
            string += "\n"
        return string
