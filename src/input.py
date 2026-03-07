import keyboard

from constants import ActionKey, CellState, Direction, GameState
from model import BattlleShipGame, Board

class InputHandler():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'handlers'):
            self.handlers = {
                ActionKey.KEY_UP: self.handle_key_up,
                ActionKey.KEY_DOWN: self.handle_key_down,
                ActionKey.KEY_LEFT: self.handle_key_left,
                ActionKey.KEY_RIGHT: self.handle_key_right,
                ActionKey.KEY_SHOOT: self.handle_key_shoot,
                ActionKey.KEY_ESC: self.handle_key_esc
            }

    def handle_input(self, input_key: ActionKey):
        input_handler = self.handlers.get(input_key)
        if input_handler:
            input_handler()

    def handle_key_up(self):
        pass

    def handle_key_down(self):
        pass    

    def handle_key_left(self):
        pass

    def handle_key_right(self):
        pass

    def handle_key_shoot(self):
        pass

    def handle_key_esc(self):
        BattlleShipGame().game_state = GameState.EXIT

    def bind_keys(self):
        for action_key in ActionKey:  
            keyboard.add_hotkey(
                action_key.value, 
                lambda action=action_key: self.handle_input(action),
                suppress=True
            )
    
    def unbind_keys(self):
        for action_key in ActionKey:
            keyboard.remove_hotkey(action_key.value)

class InGameInputHandler(InputHandler):
    _instance = None
    
    def __new__(cls, board: Board = None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self, board: Board = None):
        super().__init__()
        if board and not hasattr(self, 'board'):
            self.board = board

    def handle_input(self, input_key: ActionKey):
        self.board.get_pointed_cell().states.remove(CellState.POINTED)
        super().handle_input(input_key)
        self.board.set_pointed_cell(self.board.get_cell(self.board.crosshair))
        self.board.update_all_cells()

    def handle_key_up(self):
        self.board.crosshair.move(Direction.UP)

    def handle_key_down(self):
        self.board.crosshair.move(Direction.DOWN)

    def handle_key_left(self):
        self.board.crosshair.move(Direction.LEFT)

    def handle_key_right(self):
        self.board.crosshair.move(Direction.RIGHT)

    def handle_key_shoot(self):
        if CellState.SHOT in self.board.get_pointed_cell().states:
                return
        self.board.get_pointed_cell().states.remove(CellState.HIDDEN)
        self.board.get_pointed_cell().states.append(CellState.REVEALED)
        self.board.get_pointed_cell().states.append(CellState.SHOT)
        
class MenuInputHandler(InputHandler):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'battle_ship_game'):
            super().__init__(BattlleShipGame())

    def handle_key_up(self):
        pass

    def handle_key_down(self):
        pass

    def handle_key_left(self):
        pass    

    def handle_key_right(self):
        pass

    def handle_key_shoot(self):
        pass

    def handle_key_esc(self):
        pass