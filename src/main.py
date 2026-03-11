import time
from model import BattleShipGame
from renderer import InGameRenderer, Renderer, EndGameRenderer, MenuRenderer
from constants import GameState
from audio import AudioManager
import keyboard

def main():
    Renderer().disable_cursor()
    try:
        battle_ship_game = BattleShipGame()
        audio = AudioManager()
        menu_music_playing = False
        while not battle_ship_game.game_state == GameState.EXIT:
            if battle_ship_game.game_state == GameState.IN_GAME:
                menu_music_playing = False
                InGameRenderer().render()
            elif battle_ship_game.game_state == GameState.END_GAME:
                EndGameRenderer().render(battle_ship_game.winner)
                while True:
                    if keyboard.is_pressed("q"):
                        battle_ship_game.game_state = GameState.EXIT
                        break
            elif battle_ship_game.game_state == GameState.MENU:
                if not menu_music_playing:
                    audio.play_menu_music()
                    menu_music_playing = True
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