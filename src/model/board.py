from constants import CellState
from .coordinate import Coordinate
from .crosshair import Crosshair
from .board_cell import BoardCell

class Board:
    def __init__(self):
        self.size = 10
        self.cells = [BoardCell(Coordinate(x, y)) for x in range(self.size) for y in range(self.size)]
        self.crosshair = Crosshair()
        cell: BoardCell = self.get_cell(self.crosshair)
        cell.states.append(CellState.POINTED)
        cell.update_cell()
    
    def get_cell(self, coordinate: Coordinate) -> BoardCell:
        return self.cells[coordinate.x * self.size + coordinate.y]
    
    def get_pointed_cell(self) -> BoardCell:
        return self.get_cell(self.crosshair)
    
    def set_pointed_cell(self, cell: BoardCell):
        cell.states.append(CellState.POINTED)
        cell.update_cell()

    def update_all_cells(self):
        for cell in self.cells:
            cell.update_cell()
