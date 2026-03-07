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
        pass
