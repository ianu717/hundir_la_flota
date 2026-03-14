import random
import threading
from audio import AudioManager
from constants import GameState, GameEvents
from constants.constants import BoardCellType, CellState, ListenerNames, PlayerType
from key_input import InGameInputHandler
from model.board_cell import BoardCell
from model.coordinate import Coordinate
from model.ship import Ship
from .board import Board, ShootingBoard, ViewBoard
from .data_logger import DataLogger
from .player import Player
from .turn import Turn
from renderer import InGameRenderer

class BattleShipGame:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'game_state'):
            self.game_state = GameState.MENU
            self.real_player = Player()
            self.machine_player = Player()
            self.machine_player.is_machine = True
            self.turn = Turn(self.real_player, self.machine_player)
            self.machine_only_mode = False
            self.data_logger = None
            self.audio_manager = AudioManager()
            self.audio_manager.subscribe_events()
            GameEvents.subscribe(ListenerNames.ON_EXIT.value, self.on_exit_event)
            GameEvents.subscribe(ListenerNames.ON_SHOOT.value, self.on_shoot_event)
            GameEvents.subscribe(ListenerNames.ON_SHIP_SUNK.value, self.on_ship_sunk_event)
            GameEvents.subscribe(ListenerNames.ON_ENEMY_SHIP_SUNK.value, self.on_ship_sunk_event)
            GameEvents.subscribe(ListenerNames.ON_ALL_SHIPS_SUNK.value, self.on_all_ships_sunk_event)
            GameEvents.subscribe(ListenerNames.ON_WATER_HIT.value, self.on_water_hit_event)
            GameEvents.subscribe(ListenerNames.ON_ENEMY_WATER_HIT.value, self.on_water_hit_event)
    
    def on_exit_event(self):
        self.game_state = GameState.EXIT
    
    def on_shoot_event(self, target_cell: BoardCell, player_type=PlayerType.REAL.value):
        renderer = InGameRenderer()
        target_board = renderer.shooting_board if player_type == PlayerType.REAL.value else renderer.view_board
        if CellState.SHOT in target_cell.states:
            return
        
        if player_type == PlayerType.REAL.value:
            target_cell.states.remove(CellState.HIDDEN)
            target_cell.states.append(CellState.REVEALED)
            target_cell.states.append(CellState.SHOT)
            target_cell.update_cell_value()
        else:
            target_cell.states.append(CellState.SHOT)
            target_cell.states.append(CellState.MACHINE_SHOT)
            target_cell.update_cell_value()

        coordinate = target_cell.coordinate
        log_player = 'jugador' if player_type == PlayerType.REAL.value else 'maquina'
        if target_cell.cell_type == BoardCellType.SHIP:
            target_ship = None
            for ship in target_board.ships:
                for ship_coordinate in ship.coordinates:
                    if coordinate.x == ship_coordinate.x and coordinate.y == ship_coordinate.y:
                        target_ship = ship
            if target_ship:
                target_ship.hits += 1
                if target_ship.is_sunk():
                    if self.data_logger:
                        self.data_logger.log_shot(log_player, coordinate.x, coordinate.y, 'hundido', target_ship.name)
                    if player_type == PlayerType.MACHINE.value:
                        GameEvents.emit(ListenerNames.ON_ENEMY_SHIP_SUNK.value, target_board, target_ship, player_type)
                        if self.game_state != GameState.EXIT:
                            self.wait_machine_turn()
                    else:
                        GameEvents.emit(ListenerNames.ON_SHIP_SUNK.value, target_board, target_ship, player_type)
                else:
                    if self.data_logger:
                        self.data_logger.log_shot(log_player, coordinate.x, coordinate.y, 'tocado', target_ship.name)
                    if player_type == PlayerType.MACHINE.value:
                        GameEvents.emit(ListenerNames.ON_ENEMY_SHIP_HIT.value, coordinate)
                        if self.game_state != GameState.EXIT:
                            self.wait_machine_turn()
                    else:
                        GameEvents.emit(ListenerNames.ON_SHIP_HIT.value, coordinate)
        else:
            if self.data_logger:
                self.data_logger.log_shot(log_player, coordinate.x, coordinate.y, 'agua')
            if player_type == PlayerType.MACHINE.value:
                GameEvents.emit(ListenerNames.ON_ENEMY_WATER_HIT.value, coordinate)
            else:
                GameEvents.emit(ListenerNames.ON_WATER_HIT.value, coordinate)
    


    def on_ship_sunk_event(self, board: Board, target_ship: Ship, player_type=PlayerType.REAL.value):
        remaining_ships = board.count_remaining_ships()
        if remaining_ships == 0:
            GameEvents.emit(ListenerNames.ON_ALL_SHIPS_SUNK.value, player_type)
    
    def on_water_hit_event(self, coordinate):
        if self.machine_only_mode:
            if self.game_state != GameState.EXIT:
                self.wait_machine_turn()
            return
        self.turn.switch_turn()
        if self.turn.active_player.is_machine:
            self.wait_machine_turn()

    def wait_machine_turn(self):
        threading.Timer(0.8, self.machine_take_turn).start()
    
    def machine_take_turn(self):
        if self.game_state == GameState.EXIT:
            return
        renderer = InGameRenderer()
        target_board = renderer.view_board
        while True:
            x = random.randint(0, target_board.size - 1)
            y = random.randint(0, target_board.size - 1)
            coordinate = Coordinate(x, y)
            cell = target_board.get_cell(coordinate)
            if CellState.SHOT in cell.states:
                continue
            GameEvents.emit(ListenerNames.ON_SHOOT.value, cell, player_type=PlayerType.MACHINE.value)
            break
            
    def on_all_ships_sunk_event(self, player_type):
        self.winner = player_type
        self.game_state = GameState.END_GAME
        if self.data_logger:
            log_winner = 'jugador' if player_type == PlayerType.REAL.value else 'maquina'
            self.data_logger.log_game_end(log_winner)
    
    def init_game(self):
        self.data_logger = DataLogger()
        view_board = ViewBoard()
        shooting_board = ShootingBoard()
        InGameRenderer(view_board, shooting_board)
        InGameInputHandler(shooting_board).bind_keys() 
        self.game_state = GameState.IN_GAME
        GameEvents.emit(ListenerNames.ON_GAME_STARTED.value)
        if self.machine_only_mode:
            self.turn.active_player = self.machine_player
            self.wait_machine_turn()
        