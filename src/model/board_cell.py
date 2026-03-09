from constants import BoardCellType, CellState
from .coordinate import Coordinate

class BoardCell:
    def __init__(self, coordinate: Coordinate):
        self.coordinate = coordinate
        self.states = [CellState.HIDDEN]
        self.cell_type = BoardCellType.WATER
        self.cell_value = f" {BoardCellType.UNEXPLORED.value} "
    
    def update_cell_value(self):
        if CellState.HIDDEN in self.states:
            if CellState.POINTED in self.states:
                self.cell_value = f"[{BoardCellType.UNEXPLORED.value}]"
            else:
                self.cell_value = f" {BoardCellType.UNEXPLORED.value} "
        elif CellState.REVEALED in self.states:
            if CellState.POINTED in self.states:
                self.cell_value = f"[{self.cell_type.value}]"
            else:
                self.cell_value = f" {self.cell_type.value} "
