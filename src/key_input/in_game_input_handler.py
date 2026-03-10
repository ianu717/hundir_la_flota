from constants import ActionKey, CellState, Direction, GameEvents, BoardCellType
from constants.constants import GameState, ListenerNames
from model import Board
from model.coordinate import Coordinate
from .input_handler import InputHandler
import time

class InGameInputHandler(InputHandler):
    _instance = None
    
    def __new__(cls, board: Board = None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self, board: Board = None):
        super().__init__(None)
        if board and not hasattr(self, 'board'):
            self.board = board

    def handle_input(self, input_key: ActionKey):
        if input_key in [ActionKey.KEY_UP, ActionKey.KEY_DOWN, ActionKey.KEY_LEFT, ActionKey.KEY_RIGHT, ActionKey.KEY_ESC]:
            self.board.get_pointed_cell().states.remove(CellState.POINTED)
            super().handle_input(input_key)
            self.board.set_pointed_cell(self.board.get_cell(self.board.crosshair))
            self.board.update_all_cells_value()
        elif input_key == ActionKey.KEY_SHOOT:
            super().handle_input(input_key)

    def handle_key_up(self):
        self.board.crosshair.move(Direction.UP)

    def handle_key_down(self):
        self.board.crosshair.move(Direction.DOWN)

    def handle_key_left(self):
        self.board.crosshair.move(Direction.LEFT)

    def handle_key_right(self):
        self.board.crosshair.move(Direction.RIGHT)
    
    def handle_key_esc(self):
        GameEvents.emit(ListenerNames.ON_EXIT.value)

    def handle_key_shoot(self):
        from model import BattleShipGame

        battle_ship_game = BattleShipGame()
        if battle_ship_game.turn.active_player.is_machine:
            return
        
        pointed_cell = self.board.get_pointed_cell()
        GameEvents.emit(ListenerNames.ON_SHOOT.value, pointed_cell, player_type='real')
