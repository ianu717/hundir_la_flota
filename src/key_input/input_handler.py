import keyboard

from constants import ActionKey, GameState

class InputHandler():
    _instance = None
    
    def __new__(cls, battle_ship_game=None):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self, battle_ship_game=None):
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
        pass

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
