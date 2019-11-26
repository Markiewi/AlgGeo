from Precision import *


class Point:
    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        if self.name:
            return self.name + '=(' + str(self.x) + ', ' + str(self.y) + ')'
        else:
            return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, other):
        if other is None:
            return False
        return abs(self.x - other.x) < Precision.EPSILON and abs(self.y - other.y) < Precision.EPSILON

    @staticmethod
    def add_multiple_points(points):
        new_points = []
        for point in points:
            if len(point) == 3:
                new_points.append(Point(point[0], point[1], point[2]))
            else:
                new_points.append(Point(point[0], point[1]))
        return new_points
