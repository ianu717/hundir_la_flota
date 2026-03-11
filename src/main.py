import time
from model import BattleShipGame
from renderer import InGameRenderer, Renderer, EndGameRenderer, MenuRenderer
from constants import GameState
import keyboard

def main():
    Renderer().disable_cursor()
    try:
        battle_ship_game = BattleShipGame()
        while not battle_ship_game.game_state == GameState.EXIT:
            if battle_ship_game.game_state == GameState.IN_GAME:
                InGameRenderer().render()
            elif battle_ship_game.game_state == GameState.END_GAME:
                EndGameRenderer().render(battle_ship_game.winner)
                while True:
                    if keyboard.is_pressed("q"):
                        battle_ship_game.game_state = GameState.EXIT
                        break
            elif battle_ship_game.game_state == GameState.MENU:
                MenuRenderer().render()
                while True:
                    if keyboard.is_pressed("p"):
                        battle_ship_game.init_game()
                        break
                    elif keyboard.is_pressed("q"):
                        battle_ship_game.game_state = GameState.EXIT    
                        break
            time.sleep(1/30)
    finally:
        Renderer().enable_cursor()
        Renderer().clear_screen()

if __name__ == "__main__":
    main()