class Face:
    def __init__(self):
        self.edge = None

    def face_vertices(self):
        if self.edge is None:
            return None

        start = self.edge.origin
        edge = self.edge.next_hedge

        vertices = [start]

        while edge.origin != start:
            vertices.append(self.edge.origin)
            edge = edge.next_hedge

        return vertices
