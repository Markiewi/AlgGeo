from LineSegment import *
from Broom import *


def Sweeping(line_segments):
    broom = Broom()

    for segment in line_segments:
        broom.heap_insert_point(segment.p, segment)
        broom.heap_insert_point(segment.q, segment)

    while len(broom.heap) > 0:
        event = broom.heap_take_min()
        broom.x = event.point.x

        if event.state == 0:
            broom.root_insert(event.segment)

            tree_node = broom.root.find(event.segment)

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

        elif event.state == 1:
            tree_node = broom.root.find(event.segment)
            if tree_node.top is not None and tree_node.bottom is not None:
                top = tree_node.top
                bottom = tree_node.bottom
            else:
                top = None
                bottom = None

            broom.root_delete(event.segment)

            if top is not None and bottom is not None:
                intersection = top.segment.check_for_intersection(bottom.segment)

                if intersection is not None and not broom.intersections_check_if_already_in(intersection):
                    broom.heap_insert_intersection(intersection, top.segment, bottom.segment)
                    broom.intersections.append(intersection)

        else:
            broom.root_intersection(event.segment, event.optional_segment)

            s1 = broom.root.find(event.segment)
            s2 = broom.root.find(event.optional_segment)

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


p = [(0, 2, 'A'), (8, 2, 'B'), (3, 3, 'C'), (7, 7, 'D'), (5, 8, 'E'), (7, 1, 'F'),
     (5, 1, 'G'), (9, 6, 'H'), (3, 4, 'I'), (10, 4, 'J'), (1, 1, 'K'), (8, 3, 'L')]
points = Point.add_multiple_points(p)
# print(points)

ls = LineSegment.add_multiple_line_segments(points)
print(ls)
intersections = Sweeping(ls)
print(len(intersections))
for inter in intersections:
    print(inter)
