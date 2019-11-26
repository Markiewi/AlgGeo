import math as m


class Vertex:
    """Minimal implementation of a vertex of a 2D dcel"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hedgelist = []

    def sort_incident_counter_clockwise(self):
        if len(self.hedgelist) < 2:
            return

        for i in range(len(self.hedgelist)):
            x = self.hedgelist[i].twin.origin.x
            y = self.hedgelist[i].twin.origin.y
            print(x, y)
        print()

    def __repr__(self):
        hedge_list = ''
        for hedge in self.hedgelist:
            hedge_list += '(' + str(hedge.twin.origin.x) + ', ' + str(hedge.twin.origin.y) + '), '

        return 'Vertex: (%s, %s)\nHedge list: %s' % (self.x, self.y, hedge_list)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Hedge:
    """Minimal implementation of a half-edge of a 2D dcel"""

    def __init__(self, v1, v2):
        # The origin is defined as the vertex it points to
        self.origin = v2
        self.twin = None
        self.face = None
        self.nexthedge  = None
        self.prevhedge  = None

    def __repr__(self):
        origin = '(' + str(self.origin.x) + ', ' + str(self.origin.y) + ')'
        next_point = '(' + str(self.twin.origin.x) + ', ' + str(self.twin.origin.y) + ')'
        return 'Origin: %s -- Next: %s' % (origin, next_point)

class Face:
    """Implements a face of a 2D dcel"""

    def __init__(self):
        self.wedge = None
        self.data = None
        self.external = None

    def area(self):
        h = self.wedge
        a = 0
        while not h.nexthedge is self.wedge:
            p1 = h.origin
            p2 = h.nexthedge.origin
            a += p1.x * p2.y - p2.x * p1.y
            h = h.nexthedge

        p1 = h.origin
        p2 = self.wedge.origin
        a = (a + p1.x * p2.y - p2.x * p1.y) / 2
        return a


class Dcel:
    def __init__(self, vl, el):
        self.vertices = []
        self.hedges = []
        self.faces = []
        self.build_dcel(vl, el)

    def build_dcel(self, vl, el):
        for v in vl:
            self.vertices.append(Vertex(v[0], v[1]))
        # print(self.vertices)


        for e in el:
            e0 = find_vertex_index(self.vertices, e[0])
            e1 = find_vertex_index(self.vertices, e[1])
            h1 = Hedge(self.vertices[e0], self.vertices[e1])
            h2 = Hedge(self.vertices[e1], self.vertices[e0])
            h1.twin = []
            h1.twin = h2
            h2.twin = []
            h2.twin = h1
            self.vertices[e1].hedgelist.append(h1)
            self.vertices[e0].hedgelist.append(h2)
            self.hedges.append(h2)
            self.hedges.append(h1)
        # for v in self.hedges:
        #     print(v, v.angle, '\n')

        for v in self.vertices:
            v.sort_incident_counter_clockwise()
        #     l = len(v.hedgelist)
        #
        #     for i in range(l-1):
        #         v.hedgelist[i].nexthedge = v.hedgelist[i+1].twin
        #         v.hedgelist[i+1].prevhedge = v.hedgelist[i]
        #     v.hedgelist[l-1].nexthedge = v.hedgelist[0].twin
        #     v.hedgelist[0].prevhedge = v.hedgelist[l-1]
        #
        # provlist = self.hedges[:]
        # nf = 0
        # nh = len(self.hedges)
        #
        # while nh > 0:
        #     h = provlist.pop()
        #     nh -= 1
        #     if h.face == None:
        #         f = Face()
        #         nf += 1
        #         f.wedge = h
        #         f.wedge.face = f
        #
        #         while not h.nexthedge is f.wedge:
        #             h = h.nexthedge
        #             h.face = f
        #         self.faces.append(f)
        #
        # for f in self.faces:
        #     f.external = f.area() < 0


# Misc. functions


def hsort(h1, h2):
    """Sorts two half edges counterclockwise"""

    if h1.angle < h2.angle:
        return -1
    elif h1.angle > h2.angle:
        return 1
    else:
        return 0


def hangle(x, y):
    """Determines the angle with respect to the x axis of a segment
    of coordinates dx and dy
    """

    l = m.sqrt(x * x + y * y)
    if y > 0:
        return m.acos(x / l)
    else:
        return 2 * m.pi - m.acos(x / l)

def find_vertex_index(vl, v):
    for i in range(len(vl)):
        if vl[i].x == v[0] and vl[i].y == v[1]:
            return i
    return None

def determinant(a, b, c):
    return a.x * b.y + a.y * c.x + b.x * c.y - b.y * c.x - a.y * b.x - a.x * c.y


p = [(2, 4), (6, 1), (6, 8), (10, 4), (13, 1), (12, 9)]
e = [[p[0], p[1]], [p[0], p[2]], [p[1], p[2]], [p[2], p[5]],
     [p[2], p[3]], [p[3], p[5]], [p[4], p[5]], [p[3], p[4]],
     [p[1], p[3]]]

dcel = Dcel(p, e)
