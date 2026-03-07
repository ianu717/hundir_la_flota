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

class ScreenControl(Enum):
    CLEAR_SCREEN = "\033[H\033[J"
    ENABLE_CURSOR = "\033[?25h"
    DISABLE_CURSOR = "\033[?25l"

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
    EXIT = "exit"

class BoardCellType(Enum):
    WATER = f"{Color.BLUE.value}~{Color.RESET.value}"
    SHIP = f"{Color.RED.value}■{Color.RESET.value}"
    UNEXPLORED = f"{Color.GREEN.value}·{Color.RESET.value}"

class CellState(Enum):
    POINTED = "pointed"
    HIDDEN = "hidden"
    REVEALED = "revealed"
    SHOT = "shot"