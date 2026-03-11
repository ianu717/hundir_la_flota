from constants.constants import PlayerType
from renderer.renderer import Renderer

class EndGameRenderer(Renderer):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
    
    def render(self, winner):
        self.clear_screen()
        if PlayerType.REAL.value == winner:
            print("Has ganado! Felicidades!")
        else:
            print("Has perdido! La maquina te ha ganado!")