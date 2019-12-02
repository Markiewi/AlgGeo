from Vertex import *
from HalfEdge import *
from Face import *


class DoublyConnectedEdgeList:
    def __init__(self, points):
        self.vertices = []
        self.hedges = []
        self.faces = []
        self.build_dcel(points)

    def build_dcel(self, points):
        size = len(points)

        face = Face()
        self.faces.append(face)

        prev_left_edge = None
        prev_right_edge = None

        for i in range(size):
            point = points[i]
            vertex = Vertex()
            left = HalfEdge()
            right = HalfEdge()

            left.face = face
            left.next_hedge = None
            left.origin = vertex
            left.twin = right

            right.face = None
            right.next_hedge = prev_right_edge
            right.origin = None
            right.twin = left

            self.hedges.append(left)
            self.hedges.append(right)

            vertex.incident_edge = left
            vertex.point = point

            self.vertices.append(vertex)

            if prev_left_edge is not None:
                prev_left_edge.next_hedge = left

            if prev_right_edge is not None:
                prev_right_edge.origin = vertex

            prev_left_edge = left
            prev_right_edge = right

        first_left_edge = self.hedges[0]
        prev_left_edge.next_hedge = first_left_edge

        first_right_edge = self.hedges[1]
        first_right_edge.next_hedge = prev_right_edge

        prev_right_edge.origin = self.vertices[0]

        face.wedge = first_left_edge

        for hedge in self.hedges:
            hedge.next_hedge.prev_hedge = hedge
