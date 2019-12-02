from Point import *


class Vertex:
    def __init__(self):
        self.point = None
        self.incident_edge = None

    def __repr__(self):
        return 'Vertex: %s\nIncident edge: %s' % (self.point, self.incident_edge)
