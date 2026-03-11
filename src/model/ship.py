from .coordinate import Coordinate


class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []
        self.hits = 0
    
    def is_sunk(self):
        return self.hits >= self.size
    
class Carrier(Ship):
    def __init__(self):
        super().__init__("Portaaviones", 5)

class Battleship(Ship):
    def __init__(self):
        super().__init__("Acorazado", 4)

class Cruiser(Ship):
    def __init__(self):
        super().__init__("Crucero", 3)

class Submarine(Ship):
    def __init__(self):
        super().__init__("Submarino", 3)

class Destroyer(Ship):
    def __init__(self):
        super().__init__("Destructor", 2)