from LineSegment import *
from Broom import *
import random


def Sweeping(line_segments):
    broom = Broom()

    for segment in line_segments:
        broom.heap_insert_point(segment.p, segment)
        broom.heap_insert_point(segment.q, segment)

    while len(broom.heap) > 0:
        event = broom.heap_take_min()
        broom.x = event.point.x

        if event.state == 0:  # event is starting point of the line segment
            broom.root_insert(event.segment)

            tree_node = broom.root.find(event.segment)

            # for the added line checking if it has intersections with its neighbours, if so add new intersection
            if tree_node.top is not None:
                intersection = tree_node.segment.check_for_intersection(tree_node.top.segment)
                if intersection is not None:
                    broom.heap_insert_intersection(intersection, tree_node.segment, tree_node.top.segment)
                    broom.intersections.append(intersection)
            if tree_node.bottom is not None:
                intersection = tree_node.segment.check_for_intersection(tree_node.bottom.segment)
                if intersection is not None:
                    broom.heap_insert_intersection(intersection, tree_node.segment, tree_node.bottom.segment)
                    broom.intersections.append(intersection)

        elif event.state == 1:  # event is the ending point of the line segment
            tree_node = broom.root.find(event.segment)
            if tree_node.top is not None and tree_node.bottom is not None:
                top = tree_node.top
                bottom = tree_node.bottom
            else:
                top = None
                bottom = None

            broom.root_delete(event.segment)

            # if the deleted line segment had both top and bottom neighbours check if the they have intersection
            if top is not None and bottom is not None:
                intersection = top.segment.check_for_intersection(bottom.segment)

                if intersection is not None and not broom.intersections_check_if_already_in(intersection):
                    broom.heap_insert_intersection(intersection, top.segment, bottom.segment)
                    broom.intersections.append(intersection)

        else:  # event is the point of intersection of two line segments
            broom.root_intersection(event.segment, event.optional_segment)

            s1 = broom.root.find(event.segment)
            s2 = broom.root.find(event.optional_segment)

            # for the swapped line segments check respectively for the new top (top in regard to the two swapped lines)
            # if it has intersection with its top neighbour (if one exists)
            # and for the new bottom if it has intersection with ts bottom neighbour (if one exists)
            if s1.top == s2:
                if s1.bottom is not None:
                    intersection = s1.segment.check_for_intersection(s1.bottom.segment)

                    if intersection is not None and not broom.intersections_check_if_already_in(intersection):
                        broom.heap_insert_intersection(intersection, s1.segment, s1.bottom.segment)
                        broom.intersections.append(intersection)

                elif s2.top is not None:
                    intersection = s2.segment.check_for_intersection(s2.top.segment)

                    if intersection is not None and not broom.intersections_check_if_already_in(intersection):
                        broom.heap_insert_intersection(intersection, s2.segment, s2.top.segment)
                        broom.intersections.append(intersection)

            elif s1.bottom == s2:
                if s1.top is not None:
                    intersection = s1.segment.check_for_intersection(s1.top.segment)

                    if intersection is not None and not broom.intersections_check_if_already_in(intersection):
                        broom.heap_insert_intersection(intersection, s1.segment, s1.top.segment)
                        broom.intersections.append(intersection)

                elif s2.bottom is not None:
                    intersection = s2.segment.check_for_intersection(s2.bottom.segment)

                    if intersection is not None and not broom.intersections_check_if_already_in(intersection):
                        broom.heap_insert_intersection(intersection, s2.segment, s2.bottom.segment)
                        broom.intersections.append(intersection)

    return broom.intersections


p1 = [(2, 12, 'A'), (24, 4, 'B'), (4, 2, 'C'), (26, 12, 'D'), (6, 8, 'E'), (7, 6, 'F'),
     (16, 12, 'G'), (18, 4, 'H'), (18, 14, 'I'), (22, 2, 'J'), (8, 5, 'K'), (10, 7, 'L')]
p2 = [(1, 5, 'A'), (100, 10, 'B'), (1, 4, 'C'), (100, 11, 'D'), (1, 3, 'E'),
      (100, 100, 'F'), (1, 2, 'G'), (100, 110, 'H')]
points = Point.add_multiple_points(p2)
# print(points)

ls = LineSegment.add_multiple_line_segments(points)
print(ls)
intersections = Sweeping(ls)
print(len(intersections))
for inter in intersections:
    print(inter)
