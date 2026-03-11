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
    END_GAME = "end_game"
    EXIT = "exit"

class PlayerType(Enum):
    REAL = "real"
    MACHINE = "machine"

class BoardCellType(Enum):
    WATER = f"{Color.BLUE.value}~{Color.RESET.value}"
    SHIP = f"{Color.CYAN.value}⏅{Color.RESET.value}"
    UNEXPLORED = f"{Color.GREEN.value}·{Color.RESET.value}"
    CROSSHAIR_LEFT = f"{Color.YELLOW.value}[{Color.RESET.value}"
    CROSSHAIR_RIGHT = f"{Color.YELLOW.value}]{Color.RESET.value}"

class CellState(Enum):
    POINTED = "pointed"
    HIDDEN = "hidden"
    REVEALED = "revealed"
    SHOT = "shot"
    MACHINE_SHOT = "machine_shot"

class ListenerNames(Enum):
    ON_EXIT = "on_exit"
    ON_GAME_STARTED = "on_game_started"
    ON_KEY_UP = "on_key_up"
    ON_KEY_DOWN = "on_key_down"
    ON_KEY_LEFT = "on_key_left"
    ON_KEY_RIGHT = "on_key_right"
    ON_CROSSHAIR_MOVED = "on_crosshair_moved"
    ON_SHOOT = "on_shoot"
    ON_SHIP_HIT = "on_ship_hit"
    ON_SHIP_SUNK = "on_ship_sunk"
    ON_WATER_HIT = "on_water_hit"
    ON_ALL_SHIPS_SUNK = "on_all_ships_sunk"
    ON_ENEMY_SHIP_HIT = "on_enemy_ship_hit"
    ON_ENEMY_SHIP_SUNK = "on_enemy_ship_sunk"
    ON_ENEMY_WATER_HIT = "on_enemy_water_hit"
