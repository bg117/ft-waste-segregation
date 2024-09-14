class Ball(object):
    
    def __init__(self, x, y, radius, orig_x, orig_y, orig_radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.diameter = radius * 2
        self.orig_x = orig_x
        self.orig_y = orig_y
        self.orig_radius = orig_radius