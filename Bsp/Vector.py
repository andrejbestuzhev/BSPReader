import ObjectHelper


# Simple 3D vector
class Vector (ObjectHelper.DefaultObject):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
