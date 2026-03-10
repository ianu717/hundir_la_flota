import random
import threading
from constants import GameState, GameEvents
from constants.constants import BoardCellType, CellState, ListenerNames
from key_input import InGameInputHandler
from model.board_cell import BoardCell
from model.coordinate import Coordinate
from model.ship import Ship
from .board import Board, ShootingBoard, ViewBoard
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
            GameEvents.subscribe(ListenerNames.ON_EXIT.value, self.on_exit_event)
            GameEvents.subscribe(ListenerNames.ON_SHOOT.value, self.on_shoot_event)
            GameEvents.subscribe(ListenerNames.ON_SHIP_HIT.value, self.on_ship_hit_event)
            GameEvents.subscribe(ListenerNames.ON_SHIP_SUNK.value, self.on_ship_sunk_event)
            GameEvents.subscribe(ListenerNames.ON_ALL_SHIPS_SUNK.value, self.on_all_ships_sunk_event)
            GameEvents.subscribe(ListenerNames.ON_WATER_HIT.value, self.on_water_hit_event)
    
    def on_exit_event(self):
        self.game_state = GameState.EXIT
    
    def on_shoot_event(self, target_cell: BoardCell, player_type='real'):
        from renderer import InGameRenderer
        from constants import BoardCellType
        renderer = InGameRenderer()
        target_board = renderer.shooting_board if player_type == 'real' else renderer.view_board
        if CellState.SHOT in target_cell.states:
            return
        
        if player_type == "real":
            target_cell.states.remove(CellState.HIDDEN)
            target_cell.states.append(CellState.REVEALED)
            target_cell.states.append(CellState.SHOT)
            target_cell.update_cell_value()
        else:
            target_cell.states.append(CellState.SHOT)
            target_cell.states.append(CellState.MACHINE_SHOT)
            target_cell.update_cell_value()

        coordinate = target_cell.coordinate
        if target_cell.cell_type == BoardCellType.SHIP:
            target_ship = None
            for ship in target_board.ships:
                for ship_coordinate in ship.coordinates:
                    if coordinate.x == ship_coordinate.x and coordinate.y == ship_coordinate.y:
                        target_ship = ship
            if target_ship:
                target_ship.hits += 1
                if target_ship.is_sunk():
                    if player_type == 'machine':
                        GameEvents.emit(ListenerNames.ON_ENEMY_SHIP_SUNK.value, target_board, target_ship)
                        if self.game_state != GameState.EXIT:
                            self.wait_machine_turn()
                    else:
                        GameEvents.emit(ListenerNames.ON_SHIP_SUNK.value, target_board, target_ship)
                else:
                    if player_type == 'machine':
                        GameEvents.emit(ListenerNames.ON_ENEMY_SHIP_HIT.value, coordinate)
                        if self.game_state != GameState.EXIT:
                            self.wait_machine_turn()
                    else:
                        GameEvents.emit(ListenerNames.ON_SHIP_HIT.value, coordinate)
        else:
            if player_type == 'machine':
                GameEvents.emit(ListenerNames.ON_ENEMY_WATER_HIT.value, coordinate)
            GameEvents.emit(ListenerNames.ON_WATER_HIT.value, coordinate)
    
    def on_ship_hit_event(self, ship_name):
        pass
    
    def on_ship_sunk_event(self, board: Board, target_ship: Ship):
        remaining_ships = board.count_remaining_ships()
        if remaining_ships == 0:
            GameEvents.emit(ListenerNames.ON_ALL_SHIPS_SUNK.value)
    
    def on_water_hit_event(self, coordinate):
        self.turn.switch_turn()
        if self.turn.active_player.is_machine:
            self.wait_machine_turn()

    def wait_machine_turn(self):
        threading.Timer(1.0, self.machine_take_turn).start()
    
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
            GameEvents.emit(ListenerNames.ON_SHOOT.value, cell, player_type='machine')
            break
            
    def on_all_ships_sunk_event(self):
        self.game_state = GameState.EXIT
    
    def init_game_state(self, new_state):
        view_board = ViewBoard()
        shooting_board = ShootingBoard()
        InGameRenderer(view_board, shooting_board)
        in_game_key_handler = InGameInputHandler(shooting_board)
        in_game_key_handler.bind_keys() 
        self.game_state = new_state

    def reset_game(self):
        self.game_state = GameState.IN_GAME
        self.turn = Turn(self.real_player, self.machine_player)