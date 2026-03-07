from model import Board, BoardCell, Coordinate
from constants import ScreenControl

class Renderer():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass

    def clear_screen(self):
        print(ScreenControl.CLEAR_SCREEN.value, end="")
    
    def enable_cursor(self):
        print(ScreenControl.ENABLE_CURSOR.value, end="")
        
    def disable_cursor(self):
        print(ScreenControl.DISABLE_CURSOR.value, end="")

    def render(self):
        pass

class MenuRenderer(Renderer):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass
        
    def render(self):
        pass

class InGameRenderer(Renderer):
    _instance = None
    
    def __new__(cls, board: Board = None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self, board: Board = None):
        if board and not hasattr(self, 'board'):
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