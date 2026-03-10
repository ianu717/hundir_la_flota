from constants import GameEvents
from constants.constants import ListenerNames
from model import Board, ShootingBoard, ViewBoard
from model import Coordinate
from model.ship import Ship
from .renderer import Renderer
from collections import deque

class InGameRenderer(Renderer):
    _instance = None
    
    def __new__(cls, view_board: ViewBoard = None, shooting_board: ShootingBoard = None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self, view_board: ViewBoard = None, shooting_board: ShootingBoard = None):
        if view_board and not hasattr(self, 'view_board'):
            self.view_board = view_board
        if shooting_board and not hasattr(self, 'shooting_board'):
            self.shooting_board = shooting_board    
        if not hasattr(self, 'player_board_renderer'):
            self.player_board_renderer = PlayerBoardRenderer(self.view_board)
            self.enemy_board_renderer = EnemyBoardRenderer(self.shooting_board)

    def render(self):
        self.clear_screen()
        in_game_screen = ""
        in_game_screen += self.player_board_renderer.render()
        in_game_screen += "\n\n"
        in_game_screen += self.enemy_board_renderer.render()
        print(in_game_screen)

class BoardRenderer:
    
    def __init__(self, board: Board, title: str, event_label: str):
        self.board = board
        self.title = title
        self.event_label = event_label
        self.event_log = deque(maxlen=1)
    
    def on_ship_hit_display(self, coordinate):
        msg = f"Barco tocado en {coordinate.get_alpha_x()}{coordinate.y}"
        self.event_log.append(msg)
    
    def on_ship_sunk_display(self, board: Board, target_ship: Ship):
        msg = f"¡Hundido! {target_ship.name} ha sido completamente destruido"
        self.event_log.append(msg)
    
    def on_all_ships_sunk_display(self):
        msg = "¡VICTORIA! Todos los barcos enemigos han sido hundidos"
        self.event_log.append(msg)
    
    def on_water_hit_display(self, coordinate):
        msg = f"Agua en {coordinate.get_alpha_x()}{coordinate.y}"
        self.event_log.append(msg)
    
    def render(self):
        board_str = f"{self.title}\n------------------------\n"
        for row in range(self.board.size):
            for col in range(self.board.size):
                cell = self.board.get_cell(Coordinate(row, col))
                board_str += cell.cell_value
            board_str += "\n"
        
        board_str += self.event_label + " "
        for event in self.event_log:
            board_str += f"{event}"
        
        return board_str

class PlayerBoardRenderer(BoardRenderer):

    def __init__(self, board: ViewBoard):
        super().__init__(board, "Tu flota", "Ultima accion enemiga:")
        GameEvents.subscribe(ListenerNames.ON_ENEMY_SHIP_HIT.value, self.on_ship_hit_display)
        GameEvents.subscribe(ListenerNames.ON_ENEMY_SHIP_SUNK.value, self.on_ship_sunk_display)
        GameEvents.subscribe(ListenerNames.ON_ENEMY_WATER_HIT.value, self.on_water_hit_display)
        GameEvents.subscribe(ListenerNames.ON_ALL_SHIPS_SUNK.value, self.on_all_ships_sunk_display)

class EnemyBoardRenderer(BoardRenderer):
    
    def __init__(self, board: ShootingBoard):
        super().__init__(board, "Flota enemiga", "Ultima accion tuya:")
        GameEvents.subscribe(ListenerNames.ON_SHIP_HIT.value, self.on_ship_hit_display)
        GameEvents.subscribe(ListenerNames.ON_SHIP_SUNK.value, self.on_ship_sunk_display)
        GameEvents.subscribe(ListenerNames.ON_WATER_HIT.value, self.on_water_hit_display)
        GameEvents.subscribe(ListenerNames.ON_ALL_SHIPS_SUNK.value, self.on_all_ships_sunk_display)
