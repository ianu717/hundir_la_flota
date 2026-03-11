# Instrucciones del juego: Hundir la Flota

## Requisitos
- Python 3.10 o superior.
- Dependencias de Python instaladas.
- Librerias necesarias: `keyboard` y `pygame`.

## Instalacion

```bash
pip install -r requirements.txt
```

## Crear ejecutable (.exe) para compartir
Puedes generar un ejecutable de Windows con todo incluido para no pedir a otros que instalen Python.

1. Instala PyInstaller:

```bash
pip install pyinstaller
```

2. Desde la raiz del proyecto, genera el ejecutable:

```bash
pyinstaller --onefile --console --name HundirLaFlota --add-data "assets;assets" src/main.py
```

3. El ejecutable final quedara en:
	- `dist/HundirLaFlota.exe`

### Nota importante para compartir
- Si usas `--onefile`, puedes compartir solo `HundirLaFlota.exe`.
- Si tu antivirus bloquea el `.exe`, firma el binario o comparte tambien el codigo fuente.

## Objetivo
Hundir todos los barcos del rival antes de que el rival hunda los tuyos.

## Preparacion de la partida
1. Ejecuta el juego desde `src/main.py`.
2. En el menu principal:
	- `P`: empezar una partida nueva.
	- `Q`: salir del juego.
3. Al comenzar, se generan dos tableros de 10x10:
	- Tu flota (tablero de tus barcos).
	- Flota enemiga (tablero al que disparas).
4. Los barcos se colocan automaticamente en posiciones validas (sin solaparse y dentro de limites).

## Controles

### Durante la partida
- `W`: mover mirilla arriba.
- `A`: mover mirilla a la izquierda.
- `S`: mover mirilla abajo.
- `D`: mover mirilla a la derecha.
- `ENTER`: disparar a la casilla seleccionada.
- `ESC`: salir de la partida.

### Pantalla final
- `Q`: salir del juego.

## Como se juega
1. Mueve la mirilla por la flota enemiga con `W/A/S/D`.
2. Pulsa `ENTER` para disparar a la casilla apuntada.
3. Cada disparo puede tener uno de estos resultados:
	- Agua: no hay barco en esa casilla.
	- Tocado: hay barco, pero no esta hundido.
	- Hundido: se impacto la ultima parte de ese barco.
4. El juego muestra en pantalla el ultimo evento de cada tablero (impacto, agua o hundimiento).

## Mecanicas importantes
- No puedes disparar dos veces a la misma casilla: si ya fue disparada, la accion se ignora.
- Si disparas al agua, el turno cambia al otro jugador.
- Si aciertas (tocado o hundido), mantienes el turno y puedes volver a disparar.
- La maquina dispara automaticamente en su turno, eligiendo una casilla valida al azar.
- Mientras sea turno de la maquina, tu disparo con `ENTER` no tiene efecto.

## Fin de la partida
La partida termina cuando uno de los jugadores ha hundido todos los barcos del oponente.
