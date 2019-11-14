from RedBlackTree import *
from Heap import *
from heapq import heappush, heappop


class Broom:
    epsilon = 14

    def __init__(self):
        self.x = 0
        self.rb_tree = None
        self.heap = None
        self.intersections = []

    def intersections_insert(self, point):
        point.round_up(self.epsilon)
        self.intersections.append(point)

    def intersections_check_if_already_in(self, point):
        point.round_up(self.epsilon)
        for p in self.intersections:
            if p.x == point.x and p.y == point.y:
                return True
        return False

    def heap_insert_point(self, point, segment):
        point.round_up(self.epsilon)
        if segment.p == point:
            state = 0
        else:
            state = 1

        if self.heap is None:
            self.heap = []

        node = HeapNode(point, segment, state)
        heappush(self.heap, node)

    def heap_insert_intersection(self, point, segment1, segment2):
        point.round_up(self.epsilon)
        if self.heap is None:
            self.heap = []

        node = HeapNode(point, segment1, 2, segment2)
        heappush(self.heap, node)

    def heap_take_min(self):
        return heappop(self.heap)

    def root_insert(self, segment, bottom_segment=None):
        self.rb_tree.insert(segment, bottom_segment)

    def root_delete(self, segment):
        self.rb_tree.delete(segment)

    def root_in_order(self):
        self.rb_tree.in_order()

    def root_find(self, segment):
        return self.rb_tree.find_node(segment)
