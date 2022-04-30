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
        self.cursors = {}
        self.grid = [[col for col in row] for row in grid]
        self.row_count = len(self.grid)
        self.col_count = max(len(row) for row in self.grid)
        cursor_index = 3
        for r in range(self.row_count):
            for c in range(self.col_count):
                cursor = self.grid[r][c][cursor_index]
                if cursor is not None:
                    self.add_cursor(Cursor(r, c, cursor))

    def add_cursor(self, cursor):
        self.cursors.add(cursor)

    def simulate(self):
        """ Returns whether this was the last step of the simulation. """

        locs = {}
        cursors = list(self.cursors)
        for cursor in cursors:
            self.cursors.remove(cursor)
            if self.grid[cursor.r][cursor.c] in language:
                (transform_fn, reproduce, _, _) = self.grid[cursor.r][cursor.c]
                if reproduce:
                    cursor = Custor(cursor.r, cursor.c, cursor.direction)
                cursor.transform(transform_fn)
                self.cursors.add(cursor)
                locs.add((r, c))

        for r, c in locs:
            (_, _, output, _) = self.grid[r][c]
            self.grid[r][c] = output

        return len(self.cursors) != 0

    def get_grid(self):
        return self.grid

if __name__ == "__main__":
    sim = Simulator([[]], {})
