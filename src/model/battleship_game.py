import os
from constants import GameState

class BattlleShipGame:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'game_state'):
            self.game_state = GameState.IN_GAME
    
    def reset_game(self):
        self.game_state = GameState.IN_GAME

    def shutdown(self):
        os._exit(0)
