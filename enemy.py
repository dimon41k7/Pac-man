from character import *

class Enemy(Character):
    def __init__(self, x, y, axis="horizontal"):
        super().__init__(x, y)
        self.axis = axis
        self.dir = 1

    def move(self, field):
        if self.axis == "horizontal":
            nx = self.x + self.dir
            if field.is_wall(self.y, nx):
                self.dir *= -1
            else:
                self.x = nx
        else:
            ny = self.y + self.dir
            if field.is_wall(ny, self.x):
                self.dir *= -1
            else:
                self.y = ny

    