from Broom import *
# from LineSegment import *
from Generator import *


def sweeping(line_segments):
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
            # broom.root_in_order()
            # print('///////')
            print(event.segment)
            print(event.bottom_segment)
            broom.root_delete(event.segment, 2)
            broom.root_in_order()
            print('///////////')
            broom.root_delete(event.bottom_segment, 2)
            # broom.root_in_order()
            # print('///////////')

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
        broom.root_in_order()
        print(broom.rb_tree.count, '\n')
    return broom.intersections_array


# p = [(1, 5, 'A'), (90, 30, 'B'), (10, 25, 'C'), (110, 20, 'D'), (15, 15, 'E'),
#      (31, 23, 'F'), (30, 21, 'G'), (35, 18, 'H'), (70, 30, 'I'), (85, 8, 'J'),
#      (80, 35, 'K'), (90, 8, 'L'), (30.5, 23, 'M'), (31, 22, 'N')]
# points = Point.add_multiple_points(p)
#
# ls = LineSegment.add_multiple_line_segments(points)

# ls = generate_lines(0, 100, 10)
# print(ls)
# print(sweeping(ls))

lines = [[(10.365002914864341, 12.041582037540122), (54.768282621704714, 21.639817543382357), 12.041582037540122], [(15.874584311622497, 3.035147957440343), (59.3448685277256, 77.78621697194637), 3.035147957440343], [(30.99561408998156, 40.89606450925979), (70.07030755049945, 2.93204191280525), 2.93204191280525], [(26.716044648351357, 28.004931510446518), (74.74525150652337, 10.650675739111692), 10.650675739111692], [(9.911837336688034, 0.23954679485501673), (88.48429408392545, 62.18094183526792), 0.23954679485501673], [(4.050804956525155, 6.989783404617455), (87.40565128787522, 48.76037538666152), 6.989783404617455], [(36.20237971450359, 42.59093512282317), (38.14066847485964, 9.284617894638869), 9.284617894638869], [(15.899361026189219, 18.433078116672064), (93.43779120586994, 19.88589061067104), 18.433078116672064], [(13.025614412251274, 56.76568660260598), (72.03066677902879, 3.6537277166188264), 56.76568660260598], [(34.560664380765104, 3.802147832509517), (55.59217722100037, 86.61586525310305), 3.802147832509517]]
ls = []
for line in lines:
    p1 = Point(line[0][0], line[0][1])
    p2 = Point(line[1][0], line[1][1])
    l = LineSegment(p1, p2)
    ls.append(l)
print(lines)
print(ls)
print(sweeping(ls))
