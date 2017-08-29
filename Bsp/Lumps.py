from struct import *
import ObjectHelper


class Lump (ObjectHelper.DefaultObject):
    DefaultSize = 16
    TotalLumps = 64

    def __init__(self, index, data):
        self.index = index
        self.offset, self.length, self.version, self.fourcc = unpack("iii4s", data)


class Brush (ObjectHelper.DefaultObject):
    def __init__(self):
        raise NotImplementedError


class BrushSide (ObjectHelper.DefaultObject):
    def __init__(self):
        raise NotImplementedError


class Vertex (ObjectHelper.DefaultObject):

    def __init__(self, vector):
        self.vector = vector

    def json(self):
        return dict(
            x=self.vector.x,
            y=self.vector.y,
            z=self.vector.z
        )


class Edge (ObjectHelper.DefaultObject):
    Size = 4

    def __init__(self, a, b):
        self.a = a
        self.b = b


class Surfedge (ObjectHelper.DefaultObject):
    Size = 4


class Face(ObjectHelper.DefaultObject):
    Size = 56

    def __init__(self, firstedge, numedges, side):
        self.firstedge = firstedge
        self.numedges = numedges
        self.side = side


class Real_face(ObjectHelper.DefaultObject):
    Vertices = []

    def __init__(self, face, edges, surfedges):

        root_point = 0
        first_point = 0
        second_point = 0
        vert_point = 0


        for x in range(0, face.numedges):
            edge_index = surfedges[face.firstedge+x][0]
            edge = edges[abs(edge_index)]
            reverse = edge_index >= 0
            if x == 0:
                root_point = edge.a if reverse else edge.b
                vert_point = edge.b if reverse else edge.a
            else:

                vert_point = edge.a if reverse else edge.b
                if vert_point == root_point:
                    continue
                else:
                    first_point = vert_point

                vert_point = edge.b if reverse else edge.b
                if vert_point == root_point:
                    continue
                else:
                    second_point = vert_point

                self.Vertices.append(root_point)
                self.Vertices.append(first_point)
                self.Vertices.append(second_point)


