class HalfEdge:
    def __init__(self):
        self.origin = None
        self.twin = None
        self.face = None
        self.next_hedge = None
        self.prev_hedge = None

    def __repr__(self):
        half_edge = str(self.origin.point) + ' -> ' + str(self.twin.origin.point)
        twin = str(self.twin.origin.point) + ' -> ' + str(self.origin.point)
        if self.next_hedge is not None:
            next_hedge = str(self.next_hedge.origin.point) + ' -> ' + str(self.next_hedge.twin.origin.point)
        else:
            next_hedge = 'None'

        if self.prev_hedge is not None:
            prev_hedge = str(self.prev_hedge.origin.point) + ' -> ' + str(self.prev_hedge.twin.origin.point)
        else:
            prev_hedge = 'None'

        return 'Half edge: %s  ,Twin: %s,  Face: %s\nNext: %s\nPrev: %s' % \
               (half_edge, twin, self.face, next_hedge, prev_hedge)
