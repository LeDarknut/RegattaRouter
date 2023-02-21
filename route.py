from geometry import *

class Route:
    
    def __init__(self, start : Point, moves = []):
        self.start = start
        self.moves = moves
        self.trace = [self.start]
        for vector in self.moves :
            self.trace.append(self.trace[-1] + vector)
    
    def move(self, vector : Vector):
        self.moves.append(vector)
        self.trace.append(self.trace[-1] + vector)

    def averageNorm(self):
        s = 0
        if len(self.moves) > 0 :
            for vector in self.moves :
                s += vector.norm()

            s /= len(self.moves)
        return s

    def current(self):
        return self.trace[-1]
    
    def export(self, f):
        return [(round(point.x * f), round(point.y * f)) for point in self.trace]
