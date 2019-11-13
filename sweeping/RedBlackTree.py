BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'


class Node:
    def __init__(self, key, color, parent, left=None, right=None):
        self.key = key
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return '{color} {key} Node'.format(color=self.color, key=self.key)

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
            parents_are_same = self.parent.key == other.parent.key and self.parent.color == other.parent.color
        return self.key == other.key and self.color == other.color and parents_are_same

    def has_children(self) -> bool:
        """ Returns a boolean indicating if the node has children """
        return bool(self.get_children_count())

    def get_children_count(self) -> int:
        """ Returns the number of NOT NIL children the node has"""
        if self.color == NIL:
            return 0
        return sum([int(self.left.color != NIL), int(self.right.color != NIL)])


class RedBlackTree:
    # every node has null nodes as children initially, create one such object for easy management
    NIL_LEAF = Node(key=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            # Used for deletion and uses the sibling's relationship with his parent as a guide to the rotation
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def insert(self, key):
        if not self.root:
            self.root = Node(key, color=BLACK, parent=None, left=self.NIL_LEAF, right=self.NIL_LEAF)
            self.count += 1
            return
        parent, node_dir = self._find_parent(key)
        # Doesn't allow duplicate keys (has to be changed)
        if node_dir is None:
            return
        new_node = Node(key=key, color=RED, parent=parent, left=self.NIL_LEAF, right=self.NIL_LEAF)
        if node_dir == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1

    def _find_parent(self, key):
        def inner_find(parent):
            if key == parent.key:  # To prevent duplicate keys (has to be changed)
                return None, None
            elif key > parent.key:
                if parent.right.color == NIL:
                    return parent, 'R'
                return inner_find(parent.right)
            elif key < parent.key:
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
        node_dir = 'L' if key < parent.key else 'R'
        parent_dir = 'L' if parent.key < grandfather.key else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = node_dir + parent_dir

        if uncle == self.NIL_LEAF or uncle.color == BLACK:
            if general_direction == 'LL':
                self._right_rotation(node, parent, grandfather, to_recolor=True)
