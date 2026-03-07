import time
from model import BattlleShipGame, Board
from renderer import InGameRenderer, Renderer
from key_input import InputHandler, InGameInputHandler
from constants import GameState

def main():
    try:
        battle_ship_game = BattlleShipGame()
        board = Board()
        Renderer().disable_cursor()
        in_game_renderer = InGameRenderer(board)
        in_game_key_handler = InGameInputHandler(board)
        in_game_key_handler.bind_keys()
        while not battle_ship_game.game_state == GameState.EXIT:
            in_game_renderer.render()
            time.sleep(1/60)
    finally:
        InputHandler().unbind_keys()
        Renderer().enable_cursor()
        Renderer().clear_screen()


if __name__ == "__main__":
    main()