import os

class Field:
    def __init__(self, grid):
        self.grid = grid

    def is_wall(self, y, x) -> bool:
        return self.grid[y][x] == "🟧"

    def eat_resource(self, y, x) -> bool:
        if self.grid[y][x] == "🔸":
            self.grid[y][x] = "　"
            return True
        return False
    
    def _eat(self, y: int, x: int, symbol: str) -> bool:
        if self.grid[y][x] == symbol:
            self.grid[y][x] = "　"
            return True
        return False

    def eat_life(self, y, x):
        return self._eat(y, x, "➕")
    
    def check_win(self):
        for row in self.grid:
            if "🔸" in row:
                return False
        return True

    @staticmethod
    def load_level(path):
        grid = []
        player_pos = None

        with open(path, encoding="utf-8") as f:
            for y, line in enumerate(f):
                row = []
                for x, ch in enumerate(line.rstrip("\n")):
                    if ch == "P":
                        player_pos = (x, y)
                        row.append("　")
                    else:
                        row.append(ch)
                grid.append(row)

        return grid, player_pos