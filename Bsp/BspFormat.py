from struct import *
from Bsp import Lumps
from Bsp import Vector

import ObjectHelper
import Resources.Messages
import json


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


# Read map objects
class Contents (ObjectHelper.DefaultObject):
    def __init__(self, header, stream):
        self.header = header
        self.stream = stream
        self.brushes = []
        self.vertexes = self.get_vertexes()
        self.edges = self.get_edges()
        self.surfedges = self.get_surfedges()
        self.faces = self.get_faces()
        self.prepare_faces()


    # Reading brush data
    def get_brushes(self):
        brush_lump = self.header.Lumps[18]
        self.stream.seek(brush_lump.offset)
        brush_data = b""
        bytes_left = brush_lump.length
        while bytes_left > 0:
            brush_data += self.stream.read(1)
            bytes_left -= 1

        print(brush_data)

    def get_vertexes(self):
        vertex_lump = self.header.Lumps[3]
        self.stream.seek(vertex_lump.offset)
        bytes_left = vertex_lump.length
        result = []
        while bytes_left > 0:
            single_vertex_data = self.stream.read(Vector.Vector.DefaultSize)
            bytes_left -= Vector.Vector.DefaultSize
            vectorx, vectory, vectorz = unpack("fff", single_vertex_data)
            vertex = Lumps.Vertex(Vector.Vector(vectorx, vectory, vectorz))
            result.append(vertex)
        print("Vertices added: {0}".format(len(result)))
        return result

    def get_edges(self):
        result = []
        edges_lump = self.header.Lumps[12]
        bytes_left = edges_lump.length
        self.stream.seek(edges_lump.offset)
        while bytes_left > 0:
            single_edge_data = self.stream.read(Lumps.Edge.Size)
            bytes_left -= Lumps.Edge.Size
            a, b = unpack("HH", single_edge_data)
            edge = Lumps.Edge(a, b)
            result.append(edge)
        print("Edges added: {0}".format(len(result)))

        return result

    def get_surfedges(self):
        result = []
        edges_lump = self.header.Lumps[13]
        bytes_left = edges_lump.length
        self.stream.seek(edges_lump.offset)
        while bytes_left > 0:
            single_surfedge_data = self.stream.read(Lumps.Surfedge.Size)
            bytes_left -= Lumps.Surfedge.Size
            surfedge = unpack("i", single_surfedge_data)
            result.append(surfedge)
        print("SurfEdges added: {0}".format(len(result)))
        return result

    def get_faces(self):
        result = []
        faces_lump = self.header.Lumps[27]
        bytes_left = faces_lump.length
        self.stream.seek(faces_lump.offset)
        while bytes_left > 0:
            single_face_data = unpack("H??ihhhh????ifiiiiiHHI", self.stream.read(Lumps.Face.Size))
            bytes_left -= Lumps.Face.Size
            face = Lumps.Face(
                single_face_data[3],
                single_face_data[4],
                single_face_data[1]
            )
            result.append(face)
        print("Faces added: {0}".format(len(result)))
        return result

    def prepare_faces(self):
        for i in range(0, len(self.faces)):
            rface = Lumps.Real_face(self.faces[i], self.edges, self.surfedges)


# Map reader class
class MapReader (ObjectHelper.DefaultObject):
    def __init__(self, binary_stream):
        self.stream = binary_stream
        self.header = False

    def load(self):
        header = Header(self.stream)
        contents = Contents(header, self.stream)
        #fp = open("result.json", "w")
        #json.dump([ob.json() for ob in contents.vertexes], fp)
        return MapData(header)


class MapData (ObjectHelper.DefaultObject):
    def __init__(self, header):
        self.header = header

