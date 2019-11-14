from Broom import *
from LineSegment import *


def sweeping(line_segments):
    epsilon = 12
    broom = Broom()

    for segment in line_segments:
        broom.heap_insert_point(point=segment.p, segment=segment)
        broom.heap_insert_point(point=segment.q, segment=segment)

    while len(broom.heap) > 0:
        event = broom.heap_take_min()
        print(event)
        broom.x = event.point.x

        if event.state == 0:
            same_key_node = broom.root_find(event.segment)

            if same_key_node is not None:
                if same_key_node.bottom_segment is not None:
                    broom.root_delete(same_key_node.bottom_segment)
                    same_key_node.bottom_segment.key = same_key_node.bottom_segment.update_key(broom.x, epsilon)
                    broom.root_insert(same_key_node.bottom_segment)

                broom.root_delete(same_key_node.segment)
                same_key_node.segment.key = same_key_node.segment.update_key(broom.x, epsilon)
                broom.root_insert(same_key_node.segment)

            broom.root_insert(event.segment)

            top = broom.root_successor(event.segment)
            bottom = broom.root_predecessor(event.segment)

            intersection = event.segment.check_for_intersection(top)
            if intersection is not None:
                intersection = intersection.round_up(epsilon)
                print('First')
                broom.intersections.append(intersection)
                broom.heap_insert_intersection(intersection, top, event.segment)
            intersection = event.segment.check_for_intersection(bottom)
            if intersection is not None:
                intersection = intersection.round_up(epsilon)
                print('Second')
                broom.intersections.append(intersection)
                broom.heap_insert_intersection(intersection, event.segment, bottom)

        elif event.state == 2:  # intersection
            broom.root_delete(event.segment)
            broom.root_delete(event.bottom_segment)

            event.segment.key = event.segment.update_key(broom.x, epsilon)
            event.bottom_segment.key = event.bottom_segment.update_key(broom.x, epsilon)

            broom.root_insert(event.bottom_segment, event.segment)

            top = broom.root_successor(event.bottom_segment)
            bottom = broom.root_predecessor(event.segment)

            intersection = event.bottom_segment.check_for_intersection(top)
            if intersection is not None:
                intersection = intersection.round_up(epsilon)
                if intersection.not_in_array(broom.intersections):
                    print('Third')
                    broom.intersections.append(intersection)
                    broom.heap_insert_intersection(intersection, top, event.bottom_segment)
            intersection = event.segment.check_for_intersection(bottom)
            if intersection is not None:
                intersection = intersection.round_up(epsilon)
                if intersection.not_in_array(broom.intersections):
                    print('Fourth')
                    broom.intersections.append(intersection)
                    broom.heap_insert_intersection(intersection, event.segment, bottom)

        else:
            same_key_node = broom.root_find(event.segment)

            if same_key_node.bottom_segment is None:
                top = broom.root_successor(same_key_node.segment)
                bottom = broom.root_predecessor(same_key_node.segment)

                broom.root_delete(same_key_node.segment)

                intersection = top.check_for_intersection(bottom)
                if intersection is not None:
                    intersection = intersection.round_up(epsilon)
                    if intersection.not_in_array(broom.intersections):
                        print('Fifth')
                        broom.intersections.append(intersection)
                        broom.heap_insert_intersection(intersection, top, bottom)
            else:
                if event.segment == same_key_node.segment:
                    broom.root_delete(same_key_node.segment)
                    top = broom.root_successor(same_key_node.bottom_segment)

                    intersection = same_key_node.bottom_segment.heap_insert_intersection(top)
                    if intersection is not None:
                        intersection = intersection.round_up(epsilon)
                        if intersection.not_in_array(broom.intersections):
                            print('Sixth')
                            broom.intersections.append(intersection)
                            broom.heap_insert_intersection(intersection, top, same_key_node.bottom_segment)
                elif event.segment == same_key_node.bottom_segment:
                    broom.root_delete(same_key_node.bottom_segment)
                    bottom = broom.root_predecessor(same_key_node.segment)

                    intersection = same_key_node.segment.heap_insert_intersection(bottom)
                    if intersection is not None:
                        intersection = intersection.round_up(epsilon)
                        if intersection.not_in_array(broom.intersections):
                            print('Seventh')
                            broom.intersections.append(intersection)
                            broom.heap_insert_intersection(intersection, same_key_node.segment, bottom)

        print(broom.heap)
        print(broom.intersections)
        broom.root_in_order()
        print()
    return broom.intersections


p = [(1, 5, 'A'), (90, 30, 'B'), (10, 25, 'C'), (110, 20, 'D'), (15, 15, 'E'),
     (25, 20, 'F'), (30, 21, 'G'), (35, 18, 'H'), (70, 30, 'I'), (85, 8, 'J'),
     (80, 35, 'K'), (90, 8, 'L')]
points = Point.add_multiple_points(p)
# print(points)

ls = LineSegment.add_multiple_line_segments(points)
print(ls)
print(sweeping(ls))
# b = Broom()
# b.root_insert(ls[0])
# b.root_insert(ls[1])
# b.root_insert(ls[2])
# b.root_in_order()
# print()
# b.root_delete(ls[2])
# b.root_in_order()
