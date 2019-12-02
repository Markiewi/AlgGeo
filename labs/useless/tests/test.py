from Point import *
from RedBlackTree import *


rb_tree = RedBlackTree()

p1 = Point(1, 2)
p2 = Point(1, 4)
rb_tree.add(p1)
rb_tree.add(p2)

for node in rb_tree:
    print(node)
