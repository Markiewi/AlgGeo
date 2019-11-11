from TreeNode import *
from HeapNode import *
from heapq import heappush, heappop


class Broom:
    def __init__(self):
        self.x = 0
        self.root = None
        self.heap = None
        self.intersections = []

    def intersections_insert(self, point):
        self.intersections.append(point)

    def intersections_check_if_already_in(self, point):
        for p in self.intersections:
            if p.x == point.x and p.y == point.y:
                return True
        return False

    def heap_insert_point(self, point, segment):
        if segment.p == point:
            state = 0
        else:
            state = 1

        if self.heap is None:
            self.heap = []

        node = HeapNode(point, segment, state)
        heappush(self.heap, node)

    def heap_insert_intersection(self, point, segment1, segment2):
        if self.heap is None:
            self.heap = []

        node = HeapNode(point, segment1, 2, segment2)
        heappush(self.heap, node)

    def heap_take_min(self):
        return heappop(self.heap)

    def root_insert(self, segment):
        if self.root is None:
            self.root = TreeNode(segment)
        else:
            self.root.insert(segment, self.x)

    def root_intersection(self, segment1, segment2):
        self.root.intersection(segment1, segment2)

    def root_delete(self, segment):
        if self.root is None:
            return None
        else:
            if self.root.find(segment) == self.root:
                root = True
            else:
                root = False
            node = self.root.delete(segment)

            if node is None:
                self.root = None
            elif root:
                node.parent = None
                self.root = node
                return node
            else:
                # return self.root.delete(segment)
                return node

    def root_in_order(self):
        if self.root is None:
            print('None')
        else:
            self.root.in_order()
