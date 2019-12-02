from Precision import *


BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'


class TreeNode:
    def __init__(self, segment, color, parent, left=None, right=None, bottom_segment=None):
        self.key = segment.key if segment is not None else None
        self.segment = segment
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right
        self.bottom_segment = bottom_segment

    def __repr__(self):
        if self.parent is not None:
            parent = str(self.parent.segment)
            parent_side = 'Left' if self.parent.left.segment == self.segment else 'Right'
        else:
            parent = 'None'
            parent_side = ''
        bottom_segment = str(self.bottom_segment) if self.bottom_segment is not None else 'None'
        return 'key: ' + str(self.key) + ' Segment: ' + str(self.segment) + \
               ' Bottom segment: ' + bottom_segment + ' Color: ' + self.color + \
               ' | ' + parent_side + ' parent: ' + parent

    def __iter__(self):
        if self.left.color != NIL:
            yield from self.left.__iter__()

        yield self.key

        if self.right.color != NIL:
            yield from self.right.__iter__()

    def __eq__(self, other):
        if self.color == NIL and self.color == other.color:
            return True
        if self.parent is None or other.parent is None:
            parents_are_same = self.parent is None and other.parent is None
        else:
            parents_are_same = abs(self.parent.key - other.parent.key) < Precision.EPSILON \
                               and self.parent.color == other.parent.color
        return (other.key is not None or (other.key is None and self.key is None)) and \
            abs(self.key - other.key) < Precision.EPSILON and self.color == other.color and parents_are_same

    def has_children(self) -> bool:
        return bool(self.get_children_count())

    def get_children_count(self) -> int:
        if self.color == NIL:
            return 0
        return sum([int(self.left.color != NIL), int(self.right.color != NIL)])

    def in_order(self):
        if self.left.color != NIL:
            self.left.in_order()
        print('N: ', self)
        if self.right.color != NIL:
            self.right.in_order()

    def update_node(self, x):
        self.segment.key = self.segment.update_key(x)
        self.key = self.segment.key
        if self.bottom_segment is not None:
            self.bottom_segment.key = self.key
