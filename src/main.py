import time
from model import BattleShipGame
from renderer import InGameRenderer, Renderer
from key_input import InputHandler
from constants import GameState

def main():
    Renderer().disable_cursor()
    try:
        battle_ship_game = BattleShipGame()
        battle_ship_game.init_game_state(GameState.IN_GAME)
        while not battle_ship_game.game_state == GameState.EXIT:
            InGameRenderer().render()
            time.sleep(1/30)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # InputHandler().unbind_keys()
        Renderer().enable_cursor()
        # Renderer().clear_screen()
    Renderer().clear_screen()

if __name__ == "__main__":
    main()