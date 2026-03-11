from .constants import ListenerNames

class GameEvents:   

    _listeners = {
        ListenerNames.ON_EXIT.value: [],
        ListenerNames.ON_KEY_UP.value: [],
        ListenerNames.ON_KEY_DOWN.value: [],
        ListenerNames.ON_KEY_LEFT.value: [],
        ListenerNames.ON_KEY_RIGHT.value: [],
        ListenerNames.ON_SHOOT.value: [],
        ListenerNames.ON_SHIP_HIT.value: [],
        ListenerNames.ON_SHIP_SUNK.value: [],
        ListenerNames.ON_WATER_HIT.value: [],
        ListenerNames.ON_ALL_SHIPS_SUNK.value: [],
        ListenerNames.ON_ENEMY_SHIP_HIT.value: [],
        ListenerNames.ON_ENEMY_SHIP_SUNK.value: [],
        ListenerNames.ON_ENEMY_WATER_HIT.value: []
    }
    
    @classmethod
    def subscribe(cls, event_name: str, callback):
        if event_name in cls._listeners:
            cls._listeners[event_name].append(callback)
    
    @classmethod
    def unsubscribe(cls, event_name: str, callback):
        if event_name in cls._listeners and callback in cls._listeners[event_name]:
            cls._listeners[event_name].remove(callback)
    
    @classmethod
    def emit(cls, event_name: str, *args, **kwargs):
        if event_name in cls._listeners:
            for callback in cls._listeners[event_name]:
                callback(*args, **kwargs)
    
    @classmethod
    def clear(cls):
        for key in cls._listeners:
            cls._listeners[key] = []
