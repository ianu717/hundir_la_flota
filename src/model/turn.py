class Turn:
    def __init__(self, player, opponent):
        self.active_player = player
        self.inactive_player = opponent
    
    def switch_turn(self):
        self.active_player, self.inactive_player = self.inactive_player, self.active_player