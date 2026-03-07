from model import BattlleShipGame
from .input_handler import InputHandler

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
