# Hundir la flota
Juego classico de hundir la flota

## Sonido

El juego reproduce efectos de sonido en Windows.

- `.wav`: se reproduce con `winsound` (sin dependencias extra)
- `.mp3` y `.ogg`: requieren `pygame` (`pip install pygame`)

Coloca tus archivos WAV en `assets/sounds/` con estos nombres:

- `crosshair_move` (`.wav`, `.mp3` o `.ogg`)
- `ship_hit` (`.wav`, `.mp3` o `.ogg`)
- `ship_sunk` (`.wav`, `.mp3` o `.ogg`)
- `water_hit` (`.wav`, `.mp3` o `.ogg`)
- `game_start` (`.wav`, `.mp3` o `.ogg`)
- `game_win` (`.wav`, `.mp3` o `.ogg`)
- `game_lose` (`.wav`, `.mp3` o `.ogg`)

Si alguno no existe todavia, el juego usa un beep provisional y sigue funcionando.
