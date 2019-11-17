from Broom import *
from LineSegment import *


def sweeping(line_segments):
    broom = Broom()

    for segment in line_segments:
        broom.heap_insert_point(point=segment.p, segment=segment)
        broom.heap_insert_point(point=segment.q, segment=segment)

    while len(broom.heap) > 0:
        event = broom.heap_take_min()
        broom.x = event.point.x

        if event.state == 0:
            same_key_node = broom.root_find(event.segment)

            if same_key_node is not None:
                if same_key_node.bottom_segment is not None:
                    broom.root_delete(same_key_node.bottom_segment)
                    same_key_node.bottom_segment.key = same_key_node.bottom_segment.update_key(broom.x)
                    broom.root_insert(same_key_node.bottom_segment)

                broom.root_delete(same_key_node.segment)
                same_key_node.segment.key = same_key_node.segment.update_key(broom.x)
                broom.root_insert(same_key_node.segment)

            broom.root_insert(event.segment)

            top = broom.root_successor(event.segment)
            bottom = broom.root_predecessor(event.segment)

            broom.intersections_insert(event.segment.check_for_intersection(top), top, event.segment)
            broom.intersections_insert(event.segment.check_for_intersection(bottom), event.segment, bottom)

        elif event.state == 2:  # intersection
            broom.root_delete(event.segment)
            broom.root_delete(event.bottom_segment)

            event.segment.key = event.segment.update_key(broom.x)
            event.bottom_segment.key = event.bottom_segment.update_key(broom.x)

            broom.root_insert(event.bottom_segment, event.segment)

            top = broom.root_successor(event.bottom_segment)
            bottom = broom.root_predecessor(event.segment)

            broom.intersections_insert(event.bottom_segment.check_for_intersection(top), top, event.bottom_segment)
            broom.intersections_insert(event.segment.check_for_intersection(bottom), event.segment, bottom)

        else:
            same_key_node = broom.root_find(event.segment)
            same_key_node = TreeNode(same_key_node.segment, same_key_node.color, same_key_node.parent,
                                     same_key_node.left, same_key_node.right, same_key_node.bottom_segment)

            if same_key_node.bottom_segment is None:
                top = broom.root_successor(same_key_node.segment)
                bottom = broom.root_predecessor(same_key_node.segment)

                broom.root_delete(same_key_node.segment)

                broom.intersections_insert(top.check_for_intersection(bottom) if top is not None else None, top, bottom)

            else:
                if event.segment == same_key_node.segment:
                    broom.root_delete(same_key_node.segment)
                    top = broom.root_successor(same_key_node.bottom_segment)

                    broom.intersections_insert(same_key_node.bottom_segment.check_for_intersection(top),
                                               top, same_key_node.bottom_segment)

                elif event.segment == same_key_node.bottom_segment:
                    broom.root_delete(same_key_node.bottom_segment)
                    bottom = broom.root_predecessor(same_key_node.segment)

                    broom.intersections_insert(same_key_node.segment.check_for_intersection(bottom),
                                               same_key_node.segment, bottom)
    return broom.intersections_array


p = [(1, 5, 'A'), (90, 30, 'B'), (10, 25, 'C'), (110, 20, 'D'), (15, 15, 'E'),
     (31, 23, 'F'), (30, 21, 'G'), (35, 18, 'H'), (70, 30, 'I'), (85, 8, 'J'),
     (80, 35, 'K'), (90, 8, 'L'), (30.5, 23, 'M'), (31, 22, 'N')]
points = Point.add_multiple_points(p)

ls = LineSegment.add_multiple_line_segments(points)
print(ls)
print(sweeping(ls))
