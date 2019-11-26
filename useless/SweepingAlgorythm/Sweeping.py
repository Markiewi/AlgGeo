from Broom import *


def sweeping(line_segments):
    broom = Broom()

    for segment in line_segments:
        broom.heap_insert_point(segment.p, segment)
        broom.heap_insert_point(segment.q, segment)

    while len(broom.events_heap) > 0:
        event = broom.heap_take_min()
        print(event)

        if abs(event.point.x - broom.x) > Precision.EPSILON:
            for intersection in broom.intersections_to_delete:
                broom.root_delete(intersection[0])
                broom.root_delete(intersection[1])
            broom.x = event.point.x - Precision.EPSILON
            for intersection in broom.intersections_to_delete:
                broom.root_insert(intersection[0])
                broom.root_insert(intersection[1])
            broom.intersections_to_delete.clear()
        broom.x = event.point.x
        broom.root_in_order()
        print('///')

        if event.state == 0:  # Beginning of the point
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
        elif event.state == 1:  # End of the point
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
        else:  # Intersection
            broom.root_delete(event.segment)
            broom.root_delete(event.bottom_segment)

            event.segment.key = event.segment.update_key(broom.x)
            event.bottom_segment.key = event.bottom_segment.update_key(broom.x)

            broom.root_insert(event.bottom_segment, event.segment)

            top = broom.root_successor(event.bottom_segment)
            bottom = broom.root_predecessor(event.segment)

            broom.intersections_insert(event.bottom_segment.check_for_intersection(top), top, event.bottom_segment)
            broom.intersections_insert(event.segment.check_for_intersection(bottom), event.segment, bottom)
        print(broom.x)
        broom.root_in_order()
        print()

    return broom.intersections_list
