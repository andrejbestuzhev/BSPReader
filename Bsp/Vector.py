import ObjectHelper


# Simple 3D vector
class Vector (ObjectHelper.DefaultObject):
    DefaultSize = 12
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
