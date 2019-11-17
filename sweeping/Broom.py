from RedBlackTree import *
from Heap import *
from heapq import heappush, heappop


class Broom:
    epsilon = 10**(-12)

    def __init__(self):
        self.x = 0
        self.rb_tree = None
        self.heap = None
        self.intersections = []

    def intersections_insert(self, point):
        for intersection in self.intersections:
            if abs(point.x - intersection.x) < self.epsilon and abs(point.y - intersection.y) < self.epsilon:
                return
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

    def root_insert(self, segment, bottom_segment=None):
        if self.rb_tree is None:
            self.rb_tree = RedBlackTree()
        self.rb_tree.insert(segment, bottom_segment, x=self.x)

    def root_delete(self, segment):
        self.rb_tree.delete(segment, x=self.x)

    def root_in_order(self):
        self.rb_tree.in_order()

    def root_find(self, segment):
        if self.rb_tree is None:
            return None
        return self.rb_tree.find_node(segment.key, x=self.x)

    def root_successor(self, segment):
        # print('Segment: ', segment)
        curr_node = self.rb_tree.find_node(segment.key, x=self.x)
        if curr_node.bottom_segment is not None and curr_node.bottom_segment == segment:
            return curr_node.segment
        else:
            succ_node = self.rb_tree.successor(curr_node)
            if succ_node is None:
                return None
            return succ_node.bottom_segment if succ_node.bottom_segment is not None else succ_node.segment

    def root_predecessor(self, segment):
        # self.root_in_order()
        # print(segment.key)
        curr_node = self.rb_tree.find_node(segment.key, x=self.x)
        if curr_node.bottom_segment is not None and curr_node.segment == segment:
            return curr_node.bottom_segment
        else:
            pred_node = self.rb_tree.predecessor(curr_node)
            if pred_node is None:
                return None
            return pred_node.segment
