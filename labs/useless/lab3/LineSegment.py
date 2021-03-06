# regular line segment with two points as reference and some useful methods


class LineSegment(object):
    def __init__(self, p, q):
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
                   str(self.q.x) + ', ' + str(self.q.y) + ')]'
        else:
            return '[(' + str(self.p.x) + ', ' + str(self.p.y) + '), (' + str(self.q.x) + ', ' + str(self.q.y) + ')]'

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
        x = self.x_of_intersection(segment)
        if x is None:
            return None

        y = self.calculate_slope() * x + self.calculate_y_intersect()

        if self.p.x <= x <= self.q.x and segment.p.x <= x <= segment.q.x:
            return Point(x, y)
        else:
            return None


# regular point with x and y coordinate along with some useful methods
class Point(object):
    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        if self.name:
            return self.name + '=(' + str(self.x) + ', ' + str(self.y) + ')'
        else:
            return '(' + str(self.x) + ', ' + str(self.y) + ')'

    @staticmethod
    def add_multiple_points(points):
        new_points = []
        for point in points:
            if len(point) == 3:
                new_points.append(Point(point[0], point[1], point[2]))
            else:
                new_points.append(Point(point[0], point[1]))
        return new_points

    def round_up(self, epsilon):
        self.x = round(self.x, epsilon)
        self.y = round(self.y, epsilon)
        return self
