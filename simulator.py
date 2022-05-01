import enum


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

    def __eq__(self, other):
        return (self.r, self.c, self.direction) == (other.r, other.c, other.direction)

    def __repr__(self):
        return f"Cursor({self.r}, {self.c}, {self.direction})"


class Simulator:
    def __init__(self, grid, language, *, cursor_style="bold"):
        counter_index = 4
        cursor_index = 3

        self.cursors = set()
        fake_lang = (None, None, None, None, 1)
        self.grid = [
            [(language.get(col, fake_lang)[counter_index], col) for col in row]
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

                cursor = self.language[char][cursor_index]
                if cursor is not None:
                    self.add_cursor(Cursor(r, c, cursor))

        self.cursor_style = cursor_style

    def add_cursor(self, cursor):
        self.cursors.add(cursor)

    def simulate(self):
        """Returns whether this was the last step of the simulation."""

        locs = set()
        cursors = list(self.cursors)
        self.cursors.clear()
        for cursor in cursors:
            if self.grid[cursor.r][cursor.c][1] in self.language:
                (transform_fn, reproduce, _, _, _) = self.language[
                    self.grid[cursor.r][cursor.c][1]
                ]
                if reproduce:
                    locs.add((cursor.r, cursor.c))
                    self.cursors.add(cursor)
                    cursor = Cursor(cursor.r, cursor.c, cursor.direction)

                cursor.transform(transform_fn)
                locs.add((cursor.r, cursor.c))
                if cursor.direction is not None:
                    cursor.move(self.row_count, self.col_count)
                    self.cursors.add(cursor)

        for r, c in locs:
            counter, current = self.grid[r][c]
            if counter == 1:
                (_, _, next_char, _, _) = self.language[current]
                counter_index = 4
                if next_char in self.language:
                    output = (self.language[next_char][counter_index], next_char)
                else:
                    output = (1, next_char)
            else:
                output = (counter - 1, current)
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
                    string += self._format_cursor(self.grid[row][col][1])
                else:
                    string += self.grid[row][col][1]
            string += "\n"
        return string

    def _format_cursor(self, char):
        style = self.cursor_style
        if style == "bold":
            return "\033[1m" + char + "\033[0m"
        if style == "inverse":
            return "\033[7m" + char + "\033[m"
        return char
