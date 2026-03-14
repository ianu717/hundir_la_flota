import csv
import os
import uuid
from datetime import datetime


class DataLogger:
    """Registra los datos de cada partida en archivos CSV para practicar data science."""

    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')
    SHOTS_FILE = 'disparos.csv'
    GAMES_FILE = 'partidas.csv'

    SHOTS_HEADERS = ['id_partida', 'turno', 'jugador', 'fila', 'columna', 'resultado', 'barco']
    GAMES_HEADERS = ['id_partida', 'ganador', 'disparos_jugador', 'disparos_maquina', 'precision_jugador', 'fecha']

    def __init__(self):
        self.game_id = str(uuid.uuid4())[:8]
        self.turn_number = 0
        self.player_shots = 0
        self.player_hits = 0
        self.machine_shots = 0
        self._ensure_data_dir()
        self._ensure_headers()

    def _ensure_data_dir(self):
        os.makedirs(self.DATA_DIR, exist_ok=True)

    def _ensure_headers(self):
        shots_path = os.path.join(self.DATA_DIR, self.SHOTS_FILE)
        games_path = os.path.join(self.DATA_DIR, self.GAMES_FILE)

        if not os.path.exists(shots_path):
            with open(shots_path, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(self.SHOTS_HEADERS)

        if not os.path.exists(games_path):
            with open(games_path, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(self.GAMES_HEADERS)

    def log_shot(self, player: str, row: int, col: int, result: str, ship_name: str = ''):
        """Registra un disparo individual.

        Args:
            player: 'jugador' o 'maquina'
            row: fila del disparo (0-9)
            col: columna del disparo (0-9)
            result: 'agua', 'tocado' o 'hundido'
            ship_name: nombre del barco si fue tocado o hundido
        """
        self.turn_number += 1
        if player == 'jugador':
            self.player_shots += 1
            if result in ('tocado', 'hundido'):
                self.player_hits += 1
        else:
            self.machine_shots += 1

        shots_path = os.path.join(self.DATA_DIR, self.SHOTS_FILE)
        with open(shots_path, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([
                self.game_id, self.turn_number, player, row, col, result, ship_name
            ])

    def log_game_end(self, winner: str):
        """Registra el resumen de la partida al terminar.

        Args:
            winner: 'jugador' o 'maquina'
        """
        hit_rate = round(self.player_hits / self.player_shots, 4) if self.player_shots > 0 else 0.0
        games_path = os.path.join(self.DATA_DIR, self.GAMES_FILE)
        with open(games_path, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([
                self.game_id,
                winner,
                self.player_shots,
                self.machine_shots,
                hit_rate,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ])
