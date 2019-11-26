from enum import Enum


class Premises:
    EPSILON = 10 ** (-12)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def to_tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        if self is None or other is None:
            return False
        return abs(self.x - other.x) < Premises.EPSILON and abs(self.y - other.y) < Premises.EPSILON

    def __hash__(self):
        return hash(self.to_tuple())

    def __lt__(self, other):
        if abs(self.x - other.x) < Premises.EPSILON:
            return self.y > other.y
        return self.x > other.x


class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def to_tuple(self):
        return self.start.to_tuple(), self.end.to_tuple()

    def __eq__(self, other):
        return self.end == other.end and self.start == other.start

    def __repr__(self):
        return '[' + str(self.start) + ', ' + str(self.end) + ']'

    def __hash__(self):
        return 13 * hash(self.start) + 53 * hash(self.end)


class EventType(Enum):
    start = 1
    end = 3
    intersection = 2

    def __lt__(self, other):
        return self.value < other.value
