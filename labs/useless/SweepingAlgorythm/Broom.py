from RedBlackTree import *
from HeapNode import *
from heapq import heappop, heappush
from PointsRedBlackTree import *


class Broom:
    def __init__(self):
        self.x = 0
        self.current_state_tree = None
        self.events_heap = None
        self.intersections_tree = None
        self.intersections_list = []
        self.intersections_to_delete = []

    def intersections_insert(self, point, segment1, segment2):
        if self.intersections_tree is None:
            self.intersections_tree = DuplicateRedBlackTree()

        if point is not None and self.intersections_tree.find_node(point) is None:
            self.intersections_tree.insert(point)
            self.heap_insert_intersection(point, segment1, segment2)
            self.intersections_list.append(point)

    def intersections_in_order(self):
        self.intersections_tree.in_order()

    def intersections_find(self, point):
        return self.intersections_tree.find_node(point)

    def heap_insert_point(self, point, segment):
        if segment.p == point:
            state = 0
        else:
            state = 1

        if self.events_heap is None:
            self.events_heap = []

        node = HeapNode(point, segment, state)
        heappush(self.events_heap, node)

    def heap_insert_intersection(self, point, segment1, segment2):
        if self.events_heap is None:
            self.events_heap = []

        node = HeapNode(point, segment1, 2, segment2)
        heappush(self.events_heap, node)

    def heap_take_min(self):
        return heappop(self.events_heap)

    def root_insert(self, segment, bottom_segment=None):
        if self.current_state_tree is None:
            self.current_state_tree = RedBlackTree()

        segment.key = segment.update_key(self.x)
        if bottom_segment is not None:
            bottom_segment.key = bottom_segment.update_key(self.x)
            self.intersections_to_delete.append((segment, bottom_segment))

        self.current_state_tree.insert(segment, bottom_segment, self.x)

    def root_delete(self, segment):
        segment.key = segment.update_key(self.x)
        self.current_state_tree.delete(segment, x=self.x)

    def root_in_order(self):
        if self.current_state_tree is None:
            return
        self.current_state_tree.in_order()

    def root_find(self, segment):
        segment.key = segment.update_key(self.x)
        if self.current_state_tree is None:
            return None
        return self.current_state_tree.find_node(segment.key, x=self.x)

    def root_successor(self, segment):
        segment.key = segment.update_key(self.x)
        curr_node = self.current_state_tree.find_node(segment.key, x=self.x)
        if curr_node.bottom_segment is not None and curr_node.bottom_segment == segment:
            return curr_node.segment
        else:
            succ_node = self.current_state_tree.successor(curr_node)
            if succ_node is None:
                return None
            return succ_node.bottom_segment if succ_node.bottom_segment is not None else succ_node.segment

    def root_predecessor(self, segment):
        segment.key = segment.update_key(self.x)
        curr_node = self.current_state_tree.find_node(segment.key, x=self.x)
        if curr_node.bottom_segment is not None and curr_node.segment == segment:
            return curr_node.bottom_segment
        else:
            pred_node = self.current_state_tree.predecessor(curr_node)
            if pred_node is None:
                return None
            return pred_node.segment
