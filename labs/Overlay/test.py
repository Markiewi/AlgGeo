from DoublyConnectedEdgeList import *
from Point import *

p = [(2, 4), (6, 1), (10, 4), (13, 1), (12, 9), (6, 8)]
e = [[p[0], p[1]], [p[0], p[2]], [p[1], p[2]], [p[2], p[5]],
     [p[2], p[3]], [p[3], p[5]], [p[4], p[5]], [p[3], p[4]],
     [p[1], p[3]]]

p = Point.to_points(p)
print(p)

dcel = DoublyConnectedEdgeList(p)
for f in dcel.faces:
    print(f.face_vertices())
