from constants import Direction
from .coordinate import Coordinate

class Crosshair(Coordinate):
    def __init__(self):
        super().__init__(0, 0)

    def move(self, direction: Direction):
        if direction == Direction.UP:
            if self.x > 0:
                self.x -= 1
        elif direction == Direction.DOWN:
            if self.x < 9:
                self.x += 1
        elif direction == Direction.LEFT:
            if self.y > 0:
                self.y -= 1
        elif direction == Direction.RIGHT:
            if self.y < 9:
                self.y += 1
