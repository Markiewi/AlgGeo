from Precision import *


BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'


class DuplicateTreeNode:
    def __init__(self, point, color, parent, left=None, right=None):
        self.key = point.x * point.y if point is not None else None
        self.point = point
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        if self.parent is not None:
            parent = str(self.parent.point)
            parent_side = 'Left' if self.parent.left.point == self.point else 'Right'
        else:
            parent = 'None'
            parent_side = ''
        return 'key: ' + str(self.key) + ' Point: ' + str(self.point) + ' Color: ' + self.color + \
               ' | ' + parent_side + ' parent: ' + parent

    def __iter__(self):
        if self.left.color != NIL:
            yield from self.left.__iter__()

        yield self.key

        if self.right.color != NIL:
            yield from self.right.__iter__()

    def __eq__(self, other):
        if self.color == NIL and self.color == other.color:
            return True
        if self.parent is None or other.parent is None:
            parents_are_same = self.parent is None and other.parent is None
        else:
            parents_are_same = abs(self.parent.key - other.parent.key) < Precision.EPSILON \
                               and self.parent.color == other.parent.color
        return (other.key is not None or (other.key is None and self.key is None)) \
            and abs(self.key - other.key) < Precision.EPSILON and self.color == other.color and parents_are_same

    def has_children(self) -> bool:
        return bool(self.get_children_count())

    def get_children_count(self) -> int:
        if self.color == NIL:
            return 0
        return sum([int(self.left.color != NIL), int(self.right.color != NIL)])

    def in_order(self):
        if self.left.color != NIL:
            self.left.in_order()
        print('N: ', self)
        if self.right.color != NIL:
            self.right.in_order()

    def get_points(self):
        intersections = []

        def get_points_inner(root):
            if root.left.color != NIL:
                get_points_inner(root.left)
            intersections.append(root.point)
            print(intersections)
            if root.right.color != NIL:
                get_points_inner(self.right)

        get_points_inner(self)
        return intersections


class DuplicateRedBlackTree:
    NIL_LEAF = DuplicateTreeNode(point=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def insert(self, point):
        key = point.x * point.y

        if not self.root:
            self.root = DuplicateTreeNode(point, color=BLACK, parent=None, left=self.NIL_LEAF, right=self.NIL_LEAF)
            self.count += 1
            return
        parent, node_dir = self._find_parent(key)
        if node_dir is None:
            return
        new_node = DuplicateTreeNode(point=point, color=RED, parent=parent, left=self.NIL_LEAF, right=self.NIL_LEAF)
        if node_dir == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1

    def _find_parent(self, key):
        def inner_find(parent):
            if key > parent.key:
                if parent.right.color == NIL:
                    return parent, 'R'
                return inner_find(parent.right)
            elif key <= parent.key:
                if parent.left.color == NIL:
                    return parent, 'L'
                return inner_find(parent.left)

        return inner_find(self.root)

    def _try_rebalance(self, node):
        parent = node.parent
        key = node.key
        if parent is None or parent.parent is None or node.color != RED or parent.color != RED:
            return
        grandfather = parent.parent
        node_dir = 'L' if key <= parent.key else 'R'
        parent_dir = 'L' if parent.key <= grandfather.key else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = node_dir + parent_dir

        if uncle == self.NIL_LEAF or uncle.color == BLACK:
            # rotate
            if general_direction == 'LL':
                self._right_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'RR':
                self._left_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'LR':
                self._right_rotation(node=None, parent=node, grandfather=parent)
                # due to the prev rotation, our node is now the parent
                self._left_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            elif general_direction == 'RL':
                self._left_rotation(node=None, parent=node, grandfather=parent)
                # due to the prev rotation, our node is now the parent
                self._right_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            else:
                raise Exception("{} is not a valid direction!".format(general_direction))
        else:  # uncle is RED
            self._recolor(grandfather)

    def _right_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_right = parent.right
        parent.right = grandfather
        grandfather.parent = parent

        grandfather.left = old_right
        old_right.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _left_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_left = parent.left
        parent.left = grandfather
        grandfather.parent = parent

        grandfather.right = old_left  # save the old left keys
        old_left.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def __update_parent(self, node, parent_old_child, new_parent):
        node.parent = new_parent
        if new_parent:
            if new_parent.key > parent_old_child.key:
                new_parent.left = node
            else:
                new_parent.right = node
        else:
            self.root = node

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def find_node(self, point):
        key = point.x * point.y

        def inner_find(root):
            if root is None or root == self.NIL_LEAF:
                return None
            if abs(key - root.key) < Precision.EPSILON and \
               abs(point.x - root.point.x) < Precision.EPSILON and abs(point.y - root.point.y) < Precision.EPSILON:
                return root
            elif key > root.key:
                return inner_find(root.right)
            elif key <= root.key:
                return inner_find(root.left)

        found_node = inner_find(self.root)
        return found_node

    def in_order(self):
        if self.root is None:
            print('None')
            return
        self.root.in_order()

    def get_points(self):
        if self.root is None:
            return
        return self.root.get_points()
