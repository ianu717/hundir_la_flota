from .renderer import Renderer

class MenuRenderer(Renderer):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass
        
    def render(self):
        self.clear_screen()
        print("""
 _   _                 _ _        _          __ _       _        
| | | |               | (_)      | |        / _| |     | |       
| |_| |_   _ _ __   __| |_ _ __  | | __ _  | |_| | ___ | |_ __ _ 
|  _  | | | | '_ \ / _` | | '__| | |/ _` | |  _| |/ _ \| __/ _` |
| | | | |_| | | | | (_| | | |    | | (_| | | | | | (_) | || (_| |       
\_| |_/\__,_|_| |_|\__,_|_|_|    |_|\__,_| |_| |_|\___/ \__\__,_|         

⠀                           |`-:_
  ,----....____            |    `+.
 (             ````----....|___   |
  \     _                      ````----....____
   \    _)                                     ```---.._
    \                                                   |
  )`.\  )`.   )`.   )`.   )`.   )`.   )`.   )`.   )`.   )`.   )`.
-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `

        """)
        print("p:Nuevo juego       q:Salir")
