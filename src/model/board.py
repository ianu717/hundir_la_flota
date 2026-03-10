from constants import CellState
from constants import BoardCellType
from .ship import Battleship, Carrier, Cruiser, Destroyer, Submarine
from .coordinate import Coordinate
from .crosshair import Crosshair
from .board_cell import BoardCell

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

    def place_ships(self):
        for ship in self.ships:
            for coordinate in ship.coordinates:
                cell = self.get_cell(coordinate)
                cell.cell_type = BoardCellType.SHIP

    def count_remaining_ships(self):
        return sum(1 for ship in self.ships if not ship.is_sunk())

class ShootingBoard(Board):
    def __init__(self):
        super().__init__()
        self.crosshair = Crosshair()
        self.cells = [BoardCell(Coordinate(x, y), [CellState.HIDDEN]) for x in range(self.size) for y in range(self.size)]
        cell: BoardCell = self.get_cell(self.crosshair)
        cell.states.append(CellState.POINTED)
        self.place_ships()
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
        self.place_ships()
        self.update_all_cells_value()