from Broom import *
from LineSegment import *


def sweeping(line_segments):
    broom = Broom()

    for segment in line_segments:
        broom.heap_insert_point(segment.p, segment)
        broom.heap_insert_point(segment.q, segment)

     while len(broom.heap) > 0:
          event = broom.heap_take_min()
          broom.x = event.point.x

          if event.state == 0:
               if broom.root_find(event.segment) is None:


p = [(1, 5, 'A'), (90, 30, 'B'), (10, 25, 'C'), (110, 20, 'D'), (15, 15, 'E'),
     (25, 20, 'F'), (30, 21, 'G'), (35, 18, 'H'), (70, 30, 'I'), (85, 8, 'J'),
     (80, 30, 'K'), (90, 8, 'L')]
points = Point.add_multiple_points(p)
# print(points)

ls = LineSegment.add_multiple_line_segments(points)
print(ls)
