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
