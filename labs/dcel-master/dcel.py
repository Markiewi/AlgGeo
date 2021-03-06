#!/usr/bin/env python
#Copyright 2008, Angel Yanguas-Gil

__all__ = ['Dcel', 'Vertex', 'Hedge', 'Face']

# from xygraph import Xygraph

import math as m

class DcelError(Exception): pass

class Vertex:
    """Minimal implementation of a vertex of a 2D dcel"""

    def __init__(self, px, py):
        self.x = px
        self.y = py
        self.hedgelist = []

    def sortincident(self):
        self.hedgelist.sort(key=lambda x: x.angle, reverse=True)

    def __repr__(self):
        return 'Len: %s, (%s, %s)' % (len(self.hedgelist), self.x, self.y)


class Hedge:
    """Minimal implementation of a half-edge of a 2D dcel"""

    def __init__(self,v1,v2):
        #The origin is defined as the vertex it points to
        self.origin = v2
        self.twin = None
        self.face = None
        self.nexthedge = None
        self.angle = hangle(v2.x-v1.x, v2.y-v1.y)
        self.prevhedge = None
        self.length = m.sqrt((v2.x-v1.x)**2 + (v2.y-v1.y)**2)

    def __repr__(self):
        return 'Origin: (%s, %s), Next: (%s, %s)' % \
               (self.origin.x, self.origin.y, self.nexthedge.origin.x, self.nexthedge.origin.y)


class Face:
    """Implements a face of a 2D dcel"""

    def __init__(self):
        self.wedge = None
        self.data = None
        self.external = None

    def __repr__(self):
        return str(self.wedge)

    def area(self):
        h = self.wedge
        a = 0
        while(not h.nexthedge is self.wedge):
            p1 = h.origin
            p2 = h.nexthedge.origin
            a += p1.x*p2.y - p2.x*p1.y
            h = h.nexthedge

        p1 = h.origin
        p2 = self.wedge.origin
        a = (a + p1.x*p2.y - p2.x*p1.y)/2
        return a

    def perimeter(self):
        h = self.wedge
        p = 0
        while (not h.nexthedge is self.wedge):
            p += h.length
            h = h.nexthedge
        return p

    def vertexlist(self):
        h = self.wedge
        pl = [h.origin]
        while(not h.nexthedge is self.wedge):
            h = h.nexthedge
            pl.append(h.origin)
        return pl

    def isinside(self, p):
        """Determines whether a point is inside a face"""

        h = self.wedge
        inside = False
        if lefton(h, p):
            while(not h.nexthedge is self.wedge):
                h = h.nexthedge
                if not lefton(h, p):
                    return False
            return True
        else:
            return False


class Dcel:
    """
    Implements a doubly-connected edge list
    """

    def __init__(self, vl=[], el=[]):
        self.vertices = []
        self.hedges = []
        self.faces = []
        if vl != []:
            self.build_dcel(vl, el)


    def build_dcel(self, vl, el):
        """
        Creates the dcel from the list of vertices and edges
        """

#Step 1: vertex list creation
        for v in vl:
            self.vertices.append(Vertex(v[0], v[1]))

#Step 2: hedge list creation. Assignment of twins and
#vertices
        for e in el:
            if e[0] >= 0 and e[1] >= 0:
                h1 = Hedge(self.vertices[e[0]], self.vertices[e[1]])
                h2 = Hedge(self.vertices[e[1]], self.vertices[e[0]])
                h1.twin = h2
                h2.twin = h1
                self.vertices[e[1]].hedgelist.append(h1)
                self.vertices[e[0]].hedgelist.append(h2)
                self.hedges.append(h2)
                self.hedges.append(h1)

        #Step 3: Identification of next and prev hedges
        for v in self.vertices:
            v.sortincident()
            l = len(v.hedgelist)
            if l < 2:
                raise DcelError(
                    "Badly formed dcel: less than two hedges in vertex")
            else:
                for i in range(l-1):
                    v.hedgelist[i].nexthedge = v.hedgelist[i+1].twin
                    v.hedgelist[i+1].prevhedge = v.hedgelist[i]
                v.hedgelist[l-1].nexthedge = v.hedgelist[0].twin
                v.hedgelist[0].prevhedge = v.hedgelist[l-1]

        #Step 4: Face assignment
        provlist = self.hedges[:]
        nf = 0
        nh = len(self.hedges)

        while nh > 0:
            h = provlist.pop()
            nh -= 1
            #We check if the hedge already points to a face
            if h.face == None:
                f = Face()
                nf += 1
                #We link the hedge to the new face
                f.wedge = h
                f.wedge.face = f
                #And we traverse the boundary of the new face
                print()
                while (not h.nexthedge is f.wedge):
                    print(h)
                    h = h.nexthedge
                    h.face = f
                self.faces.append(f)
        #And finally we have to determine the external face
        for f in self.faces:
            f.external = f.area() < 0


    def findpoints(self, pl, onetoone=False):
        """Given a list of points pl, returns a list of
        with the corresponding face each point belongs to and
        None if it is outside the map.

        """

        ans = []
        if onetoone:
            fl = self.faces[:]
            for p in pl:
                found = False
                for f in fl:
                    if f.external:
                        continue
                    if f.isinside(p):
                        fl.remove(f)
                        found = True
                        ans.append(f)
                        break
                if not found:
                    ans.append(None)

        else:
            for p in pl:
                found = False
                for f in self.faces:
                    if f.external:
                        continue
                    if f.isinside(p):
                        found = True
                        ans.append(f)
                        break
                if not found:
                    ans.append(None)

        return ans

    # def load(self, filename):
    #     """reads a dcel from file using xygraph file format"""
    #     a = Xygraph.load(self, filename)
    #     self.build_dcel()
    #     return a

    def areas(self):
        return [f.area() for f in self.faces if not f.external]

    def perimeters(self):
        return [f.perimeter() for f in self.faces if not f.external]

    def nfaces(self):
        return len(self.faces)

    def nvertices(self):
        return len(self.vertices)

    def nedges(self):
        return len(self.hedges)/2

#Misc. functions


def hsort(h1, h2):
    """Sorts two half edges counterclockwise"""

    if h1.angle < h2.angle:
        return -1
    elif h1.angle > h2.angle:
        return 1
    else:
        return 0


def checkhedges(hl):
    """Consistency check of a hedge list: nexthedge, prevhedge"""

    for h in hl:
        if h.nexthedge not in hl or h.prevhedge not in hl:
            raise DcelError("Problems with an orphan hedge...")


def area2(hedge, point):
    """Determines the area of the triangle formed by a hedge and
    an external point"""

    pa = hedge.twin.origin
    pb=hedge.origin
    pc=point
    return (pb.x - pa.x)*(pc[1] - pa.y) - (pc[0] - pa.x)*(pb.y - pa.y)


def lefton(hedge, point):
    """Determines if a point is to the left of a hedge"""

    return area2(hedge, point) >= 0


def hangle(dx,dy):
    """Determines the angle with respect to the x axis of a segment
    of coordinates dx and dy
    """

    l = m.sqrt(dx*dx + dy*dy)
    if dy > 0:
        return m.acos(dx/l)
    else:
        return 2*m.pi - m.acos(dx/l)


# if __name__=='__main__':
#     import sys
#     d = Dcel()
#     d.load(sys.argv[1])
#     for a,p in zip(d.areas(), d.perimeters()):
#         print(a, p)

# vl = [(1, 5), (4, 2), (5, 5)]
# el = [(0, 1), (0, 2), (1, 2)]

# vl = [(2, 10), (1, 4), (7, 1), (14, 5), (15, 8), (8, 12), (3, 8), (4, 5),(10, 5), (11, 7), (9, 9)]
# el = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5), (6, 7), (7, 8), (8, 9), (9, 10), (6, 10)]
#
# d = Dcel(vl, el)
# print(d.vertices, '\n')
# for hedge in d.hedges:
#     print(hedge)
# print()
# for face in d.faces:
#     print(face.vertexlist())

el = [(0, 1), (1, 2), (4, 5), (0, 5), (6, 7), (8, 9), (9, 10), (11, 12), (13, 14), (14, 15), (14, 17), (16, 17), (18, 19), (20, 21), (21, 22), (12, 23), (23, 11), (12, 24), (24, 13), (11, 25), (25, 15), (15, 26), (26, 14), (13, 27), (27, 20), (10, 28), (28, 9), (5, 29), (29, 4), (2, 30), (30, 3), (3, 31), (31, 4), (6, 23), (25, 10), (23, 25), (7, 24), (26, 8), (24, 26), (2, 27), (27, 3), (15, 28), (28, 16), (11, 29), (29, 22), (14, 30), (30, 19), (16, 31), (31, 18)]
vl = [(2, 10), (1, 4), (7, 1), (14, 5), (15, 8), (8, 12), (3, 8), (4, 5), (10, 5), (11, 7), (9, 9), (5, 10), (4, 7), (7, 3), (8, 4), (7, 8), (12, 8), (13, 6), (16, 6), (14, 3), (16, 1), (19, 7), (17, 11), (4.411764705882353, 8.235294117647058), (5.5, 5.0), (6.428571428571429, 8.571428571428571), (7.75, 5.0), (9.52, 2.44), (10.0, 8.0), (10.672727272727272, 10.472727272727273), (11.290322580645162, 3.4516129032258065), (14.571428571428571, 6.714285714285714)]
d = Dcel(vl, el)
print(len(d.faces))
