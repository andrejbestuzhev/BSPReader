from struct import *
from Bsp import Lumps

import ObjectHelper
import Resources.Messages


# Header parser class
class Header (ObjectHelper.DefaultObject):
    def __init__(self, stream):
        self.Lumps = []
        self.ident, self.version = unpack("ii", stream.read(8))
        if pack("i", self.ident).decode() == 'VBSP':
            print(Resources.Messages.Header.FileCorrect)
        else:
            raise Exception(Resources.Messages.Header.FileIncorrect)
        print("Version: {0}".format(self.version))

        for index in range(0, Lumps.Lump.TotalLumps):
            lump = Lumps.Lump(index, stream.read(Lumps.Lump.DefaultSize))
            self.Lumps.append(lump)
            print(lump)


# Map reader class
class MapReader (ObjectHelper.DefaultObject):
    def __init__(self, binary_stream):
        self.stream = binary_stream
        self.header = False

    def load(self):
        return MapData(Header(self.stream))


class MapData (ObjectHelper.DefaultObject):
    def __init__(self, header):
        self.header = header
