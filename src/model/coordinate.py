class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_alpha_x(self):
        return chr(self.x + 65)  # Convertir a letra (A=0, B=1, ...)