import os
import keyboard
from enum import Enum

class Color(Enum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

class ActionKey(Enum):
    KEY_UP = "w"
    KEY_DOWN = "s"
    KEY_LEFT = "a"
    KEY_RIGHT = "d"
    KEY_SHOOT = "enter"
    KEY_ESC = "esc"

class Direction(Enum):
    UP = '↑'
    DOWN = '↓'
    LEFT = '←'
    RIGHT = '→'

class GameState(Enum):
    MENU = "menu"
    IN_GAME = "in_game"

class BoardCellType(Enum):
    WATER = f"{Color.BLUE.value}~{Color.RESET.value}"
    SHIP = f"{Color.RED.value}■{Color.RESET.value}"
    UNEXPLORED = f"{Color.GREEN.value}·{Color.RESET.value}"

class CellState(Enum):
    POINTED = "pointed"
    HIDDEN = "hidden"
    REVEALED = "revealed"
    SHOT = "shot"

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

class Board:
    def __init__(self):
        self.size = 10
        self.cells = [BoardCell(Coordinate(x, y)) for x in range(self.size) for y in range(self.size)]
        self.crosshair = Crosshair()
        cell = self.get_cell(self.crosshair)
        cell.states.append(CellState.POINTED)
        cell.update_cell()
    
    def get_cell(self, coordinate: Coordinate):
        return self.cells[coordinate.x * self.size + coordinate.y]
    
    def get_pointed_cell(self):
        return self.get_cell(self.crosshair)
    
    def set_pointed_cell(self, cell: BoardCell):
        cell.states.append(CellState.POINTED)

    def update_all_cells(self):
        for cell in self.cells:
            cell.update_cell()

class ScreenRenderer:
    def __init__(self):
        pass

    def clear_screen(self):
        os.system("cls")
    
class InGameRenderer(ScreenRenderer):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
    
    def render(self):
        self.clear_screen()
        in_game_screen = ""
        for row in range(self.board.size):
            for col in range(self.board.size):
                cell = self.board.get_cell(Coordinate(row, col))
                in_game_screen += cell.cell_value
            in_game_screen += "\n"
        print(in_game_screen)

    def is_crosshair_cell(self, cell: BoardCell):
        return cell.coordinate.x == self.board.crosshair.coordinate.x and cell.coordinate.y == self.board.crosshair.coordinate.y

class MenuRenderer(ScreenRenderer):
    def __init__(self):
        super().__init__()
    
    def render(self):
        pass

def main():
    board = Board()
    in_game_renderer = InGameRenderer(board)
    in_game_renderer.render()
    for key in ActionKey:
        if key == ActionKey.KEY_ESC:
            keyboard.add_hotkey(key.value, shutdown, suppress=True)
        else:
            keyboard.add_hotkey(key.value, lambda action=key: in_game_key_handler(action, board, in_game_renderer), suppress=True)
    keyboard.wait()

def shutdown():
    keyboard.unhook_all()
    os._exit(0)

def menu_key_handler(event):
    pass

def in_game_key_handler(action: ActionKey, board: Board, in_game_renderer: InGameRenderer):
    match action:  
        case ActionKey.KEY_UP:
            board.get_pointed_cell().states.remove(CellState.POINTED)
            board.crosshair.move(Direction.UP)
            board.set_pointed_cell(board.get_cell(board.crosshair))
        case ActionKey.KEY_LEFT:
            board.get_pointed_cell().states.remove(CellState.POINTED)
            board.crosshair.move(Direction.LEFT)
            board.set_pointed_cell(board.get_cell(board.crosshair))
        case ActionKey.KEY_DOWN:
            board.get_pointed_cell().states.remove(CellState.POINTED)
            board.crosshair.move(Direction.DOWN)
            board.set_pointed_cell(board.get_cell(board.crosshair))
        case ActionKey.KEY_RIGHT:
            board.get_pointed_cell().states.remove(CellState.POINTED)
            board.crosshair.move(Direction.RIGHT)
            board.set_pointed_cell(board.get_cell(board.crosshair))
        case ActionKey.KEY_SHOOT:
            if CellState.SHOT in board.get_pointed_cell().states:
                return
            board.get_pointed_cell().states.remove(CellState.HIDDEN)
            board.get_pointed_cell().states.append(CellState.REVEALED)
            board.get_pointed_cell().states.append(CellState.SHOT)
        case _:
            pass
    board.update_all_cells()
    in_game_renderer.render()

if __name__ == "__main__":
    main()