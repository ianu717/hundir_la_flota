from constants import BoardCellType, CellState, Direction, GameState

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

class BoardCell:
    def __init__(self, coordinate: Coordinate):
        self.coordinate = coordinate
        self.states = [CellState.HIDDEN]
        self.cell_type = BoardCellType.WATER
        self.cell_value = f" {BoardCellType.UNEXPLORED.value} "
    
    def update_cell(self):
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

class Player:
    def __init__(self):
        self.board = Board()

class BattlleShipGame:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'game_state'):
            self.game_state = GameState.IN_GAME
    
    def reset_game(self):
        self.game_state = GameState.IN_GAME
