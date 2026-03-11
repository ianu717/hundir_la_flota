import threading
from pathlib import Path

from constants import GameEvents, ListenerNames, PlayerType

try:
    import winsound
except ImportError:
    winsound = None

try:
    import pygame
except ImportError:
    pygame = None


class AudioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return

        self.initialized = True
        self.sounds_path = Path(__file__).resolve().parents[2] / "assets" / "sounds"
        self.supported_extensions = (".wav", ".mp3", ".ogg")
        self.sound_map = {
            ListenerNames.ON_CROSSHAIR_MOVED.value: ("crosshair_move", (660, 35)),
            ListenerNames.ON_SHIP_HIT.value: ("ship_hit", (880, 90)),
            ListenerNames.ON_SHIP_SUNK.value: ("ship_sunk", (440, 220)),
            ListenerNames.ON_WATER_HIT.value: ("water_hit", (360, 80)),
            ListenerNames.ON_GAME_STARTED.value: ("game_start", (520, 140)),
            "on_game_won": ("game_win", (980, 260)),
            "on_game_lost": ("game_lose", (220, 320)),
        }
        self._subscribed = False
        self._pygame_ready = False

    def subscribe_events(self):
        if self._subscribed:
            return

        GameEvents.subscribe(ListenerNames.ON_CROSSHAIR_MOVED.value, self.play_crosshair_move)
        GameEvents.subscribe(ListenerNames.ON_SHIP_HIT.value, self.play_ship_hit)
        GameEvents.subscribe(ListenerNames.ON_SHIP_SUNK.value, self.play_ship_sunk)
        GameEvents.subscribe(ListenerNames.ON_WATER_HIT.value, self.play_water_hit)
        GameEvents.subscribe(ListenerNames.ON_ENEMY_SHIP_HIT.value, self.play_ship_hit)
        GameEvents.subscribe(ListenerNames.ON_ENEMY_SHIP_SUNK.value, self.play_ship_sunk)
        GameEvents.subscribe(ListenerNames.ON_ENEMY_WATER_HIT.value, self.play_water_hit)
        GameEvents.subscribe(ListenerNames.ON_GAME_STARTED.value, self.play_game_started)
        GameEvents.subscribe(ListenerNames.ON_ALL_SHIPS_SUNK.value, self.play_game_result)
        self._subscribed = True

    def play_menu_music(self):
        sound_file = self._resolve_sound_file("menu_music")
        if sound_file is None:
            return
        self._ensure_pygame()
        if not self._pygame_ready:
            return
        try:
            pygame.mixer.music.load(str(sound_file))
            pygame.mixer.music.play(loops=-1)
        except pygame.error:
            pass

    def stop_menu_music(self, *_args, **_kwargs):
        if not self._pygame_ready:
            return
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

    def play_crosshair_move(self):
        self._play_sound(ListenerNames.ON_CROSSHAIR_MOVED.value)

    def play_ship_hit(self, *_args, **_kwargs):
        self._play_sound(ListenerNames.ON_SHIP_HIT.value)

    def play_ship_sunk(self, *_args, **_kwargs):
        self._play_sound(ListenerNames.ON_SHIP_SUNK.value)

    def play_water_hit(self, *_args, **_kwargs):
        self._play_sound(ListenerNames.ON_WATER_HIT.value)

    def play_game_started(self, *_args, **_kwargs):
        self.stop_menu_music()
        self._play_sound(ListenerNames.ON_GAME_STARTED.value)

    def play_game_result(self, player_type, *_args, **_kwargs):
        if player_type == PlayerType.REAL.value:
            self._play_sound("on_game_won")
            return
        self._play_sound("on_game_lost")

    def _play_sound(self, event_name: str):
        sound_stem, fallback_tone = self.sound_map[event_name]
        threading.Thread(
            target=self._play_async,
            args=(sound_stem, fallback_tone),
            daemon=True,
        ).start()

    def _play_async(self, sound_stem: str, fallback_tone):
        sound_file = self._resolve_sound_file(sound_stem)
        try:
            if sound_file and sound_file.suffix.lower() == ".wav" and winsound is not None:
                winsound.PlaySound(
                    str(sound_file),
                    winsound.SND_FILENAME,
                )
                return

            if sound_file and self._play_with_pygame(sound_file):
                return
        except RuntimeError:
            pass

        if winsound is None:
            return

        frequency, duration = fallback_tone
        winsound.Beep(frequency, duration)

    def _resolve_sound_file(self, sound_stem: str):
        for extension in self.supported_extensions:
            candidate = self.sounds_path / f"{sound_stem}{extension}"
            if candidate.exists():
                return candidate
        return None

    def _ensure_pygame(self):
        if self._pygame_ready or pygame is None:
            return
        try:
            pygame.mixer.init()
            self._pygame_ready = True
        except pygame.error:
            pass

    def _play_with_pygame(self, sound_file: Path):
        if pygame is None:
            return False

        self._ensure_pygame()
        if not self._pygame_ready:
            return False

        try:
            effect = pygame.mixer.Sound(str(sound_file))
            effect.play()
            return True
        except pygame.error:
            return False