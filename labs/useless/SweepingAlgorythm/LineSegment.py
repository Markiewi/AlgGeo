from Point import *


class LineSegment:
    def __init__(self, p, q):
        self.key = p.y

        if p == q:
            raise ValueError("Line cannot be made with two identical points")
        if p.x <= q.x:
            self.p = p
            self.q = q
        else:
            self.p = q
            self.q = p

    def __repr__(self):
        if self.p.name and self.q.name:
            return '|' + self.p.name + self.q.name + '|=[(' + str(self.p.x) + ', ' + str(self.p.y) + '), (' + \
                   str(self.q.x) + ', ' + str(self.q.y) + '),' + str(self.key) + ']'
        else:
            return '[(' + str(self.p.x) + ', ' + str(self.p.y) + '), (' + str(self.q.x) + ', ' + \
                   str(self.q.y) + '), ' + str(self.key) + ']'

    def __eq__(self, other):
        if other is None:
            return False
        return (self.p == other.p and self.q == other.q) or (self.p == other.q and self.q == other.p)

    def calculate_slope(self):
        if self.p.x == self.q.x:
            return None

        return (self.p.y - self.q.y) / (self.p.x - self.q.x)

    def calculate_y_intersect(self):
        a = self.calculate_slope()

        if a is None:
            return None
        else:
            return self.p.y - a * self.p.x

    def normal_form(self):
        if self.p.x == self.q.x:
            return 'x = ' + str(self.p.x)
        elif self.p.y == self.q.y:
            return 'y = ' + str(self.p.y)
        else:
            a = self.calculate_slope()
            b = self.p.y - a * self.p.x

            if b > 0:
                b = '+ ' + str(b)
            else:
                b = '- ' + str(abs(b))

            return 'y = ' + str(a) + 'x ' + b

    @staticmethod
    def add_multiple_line_segments(points):
        if len(points) % 2 == 1:
            raise ValueError("The number of points must be even.")

        line_segments = []
        for i in range(1, len(points), 2):
            line_segments.append(LineSegment(points[i-1], points[i]))
        return line_segments

    def x_of_intersection(self, segment):
        a1 = self.calculate_slope()
        a2 = segment.calculate_slope()
        if a1 == a2:
            return None
        b1 = self.calculate_y_intersect()
        b2 = segment.calculate_y_intersect()

        return (b2 - b1) / (a1 - a2)

    def check_for_intersection(self, segment):
        if self is None or segment is None:
            return None

        x = self.x_of_intersection(segment)
        if x is None:
            return None

        y = self.calculate_slope() * x + self.calculate_y_intersect()

        if self.p.x <= x <= self.q.x and segment.p.x <= x <= segment.q.x:
            return Point(x, y)
        else:
            return None

    def update_key(self, x):
        a = self.calculate_slope()
        b = self.calculate_y_intersect()
        return a * x + b

    def lines_overlap(self, other):
        a1 = self.calculate_slope()
        a2 = other.calculate_slope()
        b1 = self.calculate_y_intersect()
        b2 = other.calculate_y_intersect()

        if abs(a1 - a2) < Precision.EPSILON and abs(b1 - b2) < Precision.EPSILON:
            if self.p.x < other.p.x < self.q.x or self.p.x < other.q.x < self.q.x:
                return True

        return False
