from constants import CellState
from constants import BoardCellType
from .ship import Battleship, Carrier, Cruiser, Destroyer, Submarine
from .coordinate import Coordinate
from .crosshair import Crosshair
from .board_cell import BoardCell
import random

class Board:
    def __init__(self):
        self.size = 10
        self.cells = []  
        self.ships = [Carrier(), Battleship(), Cruiser(), Submarine(), Destroyer()]

    def get_cell(self, coordinate: Coordinate) -> BoardCell:
        return self.cells[coordinate.x * self.size + coordinate.y]

    def update_all_cells_value(self):
        for cell in self.cells:
            cell.update_cell_value()

    def place_ship(self, ship):
        for coordinate in ship.coordinates:
            cell = self.get_cell(coordinate)
            cell.cell_type = BoardCellType.SHIP

    def place_all_ships(self):
        for ship in self.ships:
            placed = False
            while not placed:
                horizontal = random.choice([True, False])
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                if horizontal:
                    coordinates = [Coordinate(x, y + i) for i in range(ship.size)]
                else:
                    coordinates = [Coordinate(x + i, y) for i in range(ship.size)]
                
                if not self.ship_collides(coordinates):
                    ship.coordinates = coordinates
                    placed = True
                    self.place_ship(ship)
    
    def ship_collides(self, coordinates):
        for coord in coordinates:
            if coord.x < 0 or coord.x >= self.size or coord.y < 0 or coord.y >= self.size:
                return True
            
            for ship in self.ships:
                for ship_coord in ship.coordinates:
                    if coord.x == ship_coord.x and coord.y == ship_coord.y:
                        return True
        
        return False

    def count_remaining_ships(self):
        return sum(1 for ship in self.ships if not ship.is_sunk())

class ShootingBoard(Board):
    def __init__(self):
        super().__init__()
        self.crosshair = Crosshair()
        self.cells = [BoardCell(Coordinate(x, y), [CellState.HIDDEN]) for x in range(self.size) for y in range(self.size)]
        cell: BoardCell = self.get_cell(self.crosshair)
        cell.states.append(CellState.POINTED)
        self.place_all_ships()
        self.update_all_cells_value()

    def get_pointed_cell(self) -> BoardCell:
        return self.get_cell(self.crosshair)
    
    def set_pointed_cell(self, cell: BoardCell):
        cell.states.append(CellState.POINTED)
        cell.update_cell_value()

class ViewBoard(Board):
    def __init__(self):
        super().__init__()
        self.cells = [BoardCell(Coordinate(x, y), [CellState.REVEALED]) for x in range(self.size) for y in range(self.size)]
        self.place_all_ships()
        self.update_all_cells_value()