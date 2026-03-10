from constants import BoardCellType, CellState, Color
from .coordinate import Coordinate

class BoardCell:
    def __init__(self, coordinate: Coordinate, states = [], cell_type=BoardCellType.WATER):
        self.coordinate = coordinate
        self.states = states
        self.cell_type = cell_type
        self.cell_value = f" {self.cell_type.value} "

    def update_cell_value(self):
        if CellState.MACHINE_SHOT in self.states:
            shot_symbol = f"{Color.YELLOW.value}X{Color.RESET.value}"
            if CellState.POINTED in self.states:
                self.cell_value = f"[{shot_symbol}]"
            else:
                self.cell_value = f" {shot_symbol} "
        elif CellState.HIDDEN in self.states:
            if CellState.POINTED in self.states:
                self.cell_value = f"[{BoardCellType.UNEXPLORED.value}]"
            else:
                self.cell_value = f" {BoardCellType.UNEXPLORED.value} "
        elif CellState.REVEALED in self.states:
            if CellState.POINTED in self.states:
                self.cell_value = f"[{self.cell_type.value}]"
            else:
                self.cell_value = f" {self.cell_type.value} "
