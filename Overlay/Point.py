class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)

    @staticmethod
    def to_points(points):
        p = []
        for point in points:
            p.append(Point(point[0], point[1]))
        return p
