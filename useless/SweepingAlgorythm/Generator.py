import random
from LineSegment import *
from Precision import *


def generate_lines(l, r, n):
    i = 0
    lines = []
    intersections = []
    while i < n:
        add_line = True

        p1 = Point(random.uniform(l, r), random.uniform(l, r))
        p2 = Point(random.uniform(l, r), random.uniform(l, r))

        s = LineSegment(p1, p2)

        if abs(s.p.x - s.q.x) < Precision.EPSILON:
            add_line = False

        if add_line:
            for line in lines:
                point = line_check(s, line, intersections)
                if point is None:
                    add_line = False
                    intersections.append(point)
        if add_line:
            lines.append(s)
            i += 1

    return lines


def line_check(l1, l2, intersections):
    #  Checking each point if they intersect on edges
    if l1.p == l2.p or l1.p == l2.q or l1.q == l2.p or l1.q == l2.q:
        return None

    if l1.lines_overlap(l2):
        return None

    point = l1.check_for_intersection(l2)
    if point is None:
        return None

    for intersection in intersections:
        if point == intersection:
            return None

    return point
