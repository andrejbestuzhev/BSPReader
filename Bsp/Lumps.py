from struct import *
import ObjectHelper


class Lump (ObjectHelper.DefaultObject):
    DefaultSize = 16
    TotalLumps = 64

    def __init__(self, index, data):
        self.index = index
        self.offset, self.length, self.version, self.fourcc = unpack("iii4s", data)

