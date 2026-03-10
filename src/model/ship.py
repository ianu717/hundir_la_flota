from .coordinate import Coordinate


class Ship:
    def __init__(self, name, size, coordinates = []):
        self.name = name
        self.size = size
        self.coordinates = coordinates
        self.hits = 0
    
    def is_sunk(self):
        return self.hits >= self.size
    
class Carrier(Ship):
    def __init__(self, coordinates = [
        Coordinate(0, 0),
        Coordinate(0, 1),
        Coordinate(0, 2),
        Coordinate(0, 3),
        Coordinate(0, 4)
        ]):
        super().__init__("Portaaviones", 5, coordinates)

class Battleship(Ship):
    def __init__(self, coordinates = [
        Coordinate(2, 0),
        Coordinate(2, 1),
        Coordinate(2, 2),
        Coordinate(2, 3)
        ]):
        super().__init__("Acorazado", 4, coordinates)

class Cruiser(Ship):
    def __init__(self, coordinates = [
        Coordinate(4, 0),
        Coordinate(4, 1),
        Coordinate(4, 2)
        ]):
        super().__init__("Crucero", 3, coordinates)

class Submarine(Ship):
    def __init__(self, coordinates = [
        Coordinate(6, 0),
        Coordinate(6, 1),
        Coordinate(6, 2)
        ]):
        super().__init__("Submarino", 3, coordinates)

class Destroyer(Ship):
    def __init__(self, coordinates = [
        Coordinate(8, 0),
        Coordinate(8, 1)
        ]):
        super().__init__("Destructor", 2, coordinates)