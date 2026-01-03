from field import Field

class Physics:
    def try_move(self, y, x, dy, dx, field):
        ny, nx = y + dy, x + dx

        if field.is_wall(ny, nx):
            return y, x, False

        return ny, nx, True