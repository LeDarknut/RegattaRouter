from math import cos, sin


class Trajectory:
    
    def __init__(self, start, step_length = 1, points = None):
        self.start = start
        self.step_length = step_length
        if points is None:
            self.points = [start]
        else:
            self.points = points
    
    def add_point(self, angle):
        x, y = self.points[-1]
        x += self.step_length * cos(angle)
        y += self.step_length * sin(angle)
        self.points.append((x, y))
    
    def round(self, f):
        return [(round(p[0] * f), round(p[1] * f)) for p in self.points]
