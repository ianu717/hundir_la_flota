from constants.constants import PlayerType
from .renderer import Renderer

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
            print("""
 _   _                                         _       
| | | |                                       | |      
| |_| | __ _ ___    __ _  __ _ _ __   __ _  __| | ___  
|  _  |/ _` / __|  / _` |/ _` | '_ \ / _` |/ _` |/ _ \ 
| | | | (_| \__ \ | (_| | (_| | | | | (_| | (_| | (_) |
\_| |_/\__,_|___/  \__, |\__,_|_| |_|\__,_|\__,_|\___/ 
                    __/ |                              
                   |___/
            """)
            print("Has destruido todos los barcos enemigos!")
            
        else:
            print("""
 _   _                                _ _     _       
| | | |                              | (_)   | |      
| |_| | __ _ ___   _ __   ___ _ __ __| |_  __| | ___  
|  _  |/ _` / __| | '_ \ / _ \ '__/ _` | |/ _` |/ _ \ 
| | | | (_| \__ \ | |_) |  __/ | | (_| | | (_| | (_) |
\_| |_/\__,_|___/ | .__/ \___|_|  \__,_|_|\__,_|\___/ 
                  | |                                 
                  |_|
            """)
            print("La maquina ha destruido todos tus barcos!")

        print()
        print("q -> Salir")