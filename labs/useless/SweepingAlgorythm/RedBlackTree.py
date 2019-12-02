from TreeNode import *


class RedBlackTree:
    NIL_LEAF = TreeNode(segment=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def insert(self, segment, bottom_segment=None, x=None):
        key = segment.key

        if not self.root:
            self.root = TreeNode(segment, color=BLACK, parent=None, left=self.NIL_LEAF,
                                 right=self.NIL_LEAF, bottom_segment=bottom_segment)
            self.count += 1
            return
        parent, node_dir = self._find_parent(key, x)
        if node_dir is None:
            return
        new_node = TreeNode(segment=segment, color=RED, parent=parent, left=self.NIL_LEAF,
                            right=self.NIL_LEAF, bottom_segment=bottom_segment)
        if node_dir == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1

    def _find_parent(self, key, x=None):
        if x is not None and abs(key - self.root.key) > Precision.EPSILON:
            self.root.update_node(x)

        def inner_find(parent):
            if x is not None:
                if parent.left.color != NIL:
                    parent.left.update_node(x)
                if parent.right.color != NIL:
                    parent.right.update_node(x)

            if abs(key - parent.key) < Precision.EPSILON:
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

    def __update_parent(self, node, parent_old_child, new_parent):
        node.parent = new_parent
        if new_parent:
            if new_parent.key > parent_old_child.key:
                new_parent.left = node
            else:
                new_parent.right = node
        else:
            self.root = node

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

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def delete(self, segment, x=None):
        key = segment.key
        node_to_remove = self.find_node(key, x)

        if node_to_remove.bottom_segment is not None:
            if node_to_remove.bottom_segment != segment:
                node_to_remove.segment = node_to_remove.bottom_segment

            node_to_remove.bottom_segment = None
            return

        if node_to_remove is None:
            return
        if node_to_remove.get_children_count() == 2:
            successor = self._find_in_order_successor(node_to_remove, x)
            node_to_remove.key = successor.key
            node_to_remove.segment = successor.segment
            node_to_remove.bottom_segment = successor.bottom_segment
            node_to_remove = successor

        self._delete(node_to_remove)
        self.count -= 1

    def _delete(self, node):
        left_child = node.left
        right_child = node.right
        not_nil_child = left_child if left_child != self.NIL_LEAF else right_child
        if node == self.root:
            if not_nil_child != self.NIL_LEAF:
                self.root = not_nil_child
                self.root.parent = None
                self.root.color = BLACK
            else:
                self.root = None
        elif node.color == RED:
            if not node.has_children():
                self._delete_leaf(node)
            else:
                raise Exception('Unexpected behavior')
        else:
            if right_child.has_children() or left_child.has_children():  # sanity check
                raise Exception('The red child of a black node with 0 or 1 children'
                                ' cannot have children, otherwise the black height of the tree becomes invalid! ')
            if not_nil_child.color == RED:
                """
                Swap the keys with the red child and remove it  (basically un-link it)
                Since we're a node with one child only, we can be sure that there are no nodes below the red child.
                """
                node.key = not_nil_child.key
                node.segment = not_nil_child.segment
                node.bottom_segment = not_nil_child.bottom_segment
                node.left = not_nil_child.left
                node.right = not_nil_child.right
            else:  # BLACK child
                # 6 cases :o
                self._delete_black_node(node)

    def _delete_leaf(self, leaf):
        if leaf.key >= leaf.parent.key:
            leaf.parent.right = self.NIL_LEAF
        else:
            leaf.parent.left = self.NIL_LEAF

    def _delete_black_node(self, node):
        """
        Loop through each case recursively until we reach a terminating case.
        What we're left with is a leaf node which is ready to be deleted without consequences
        """
        self.__case_1(node)
        self._delete_leaf(node)

    def __case_1(self, node):
        if self.root == node:
            node.color = BLACK
            return
        self.__case_2(node)

    def __case_2(self, node):
        parent = node.parent
        sibling, direction = self._get_sibling(node)
        if sibling.color == RED and parent.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=parent)
            parent.color = RED
            sibling.color = BLACK
            return self.__case_1(node)
        self.__case_3(node)

    def __case_3(self, node):
        parent = node.parent
        sibling, _ = self._get_sibling(node)
        if (sibling.color == BLACK and parent.color == BLACK
                and sibling.left.color != RED and sibling.right.color != RED):
            # color the sibling red and forward the double black node upwards
            # (call the cases again for the parent)
            sibling.color = RED
            return self.__case_1(parent)  # start again

        self.__case_4(node)

    def __case_4(self, node):
        parent = node.parent
        if parent.color == RED:
            sibling, direction = self._get_sibling(node)
            if sibling.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
                parent.color, sibling.color = sibling.color, parent.color  # switch colors
                return  # Terminating
        self.__case_5(node)

    def __case_5(self, node):
        sibling, direction = self._get_sibling(node)
        closer_node = sibling.right if direction == 'L' else sibling.left
        outer_node = sibling.left if direction == 'L' else sibling.right
        if closer_node.color == RED and outer_node.color != RED and sibling.color == BLACK:
            if direction == 'L':
                self._left_rotation(node=None, parent=closer_node, grandfather=sibling)
            else:
                self._right_rotation(node=None, parent=closer_node, grandfather=sibling)
            closer_node.color = BLACK
            sibling.color = RED

        self.__case_6(node)

    def __case_6(self, node):
        sibling, direction = self._get_sibling(node)
        outer_node = sibling.left if direction == 'L' else sibling.right

        def __case_6_rotation(direction):
            parent_color = sibling.parent.color
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=sibling.parent)
            # new parent is sibling
            sibling.color = parent_color
            sibling.right.color = BLACK
            sibling.left.color = BLACK

        if sibling.color == BLACK and outer_node.color == RED:
            return __case_6_rotation(direction)  # terminating

        raise Exception('We should have ended here, something is wrong')

    def _find_in_order_successor(self, node, x=None):
        if x is not None:
            node.update_node(x)
            if node.right is not None and node.right.color != NIL:
                node.right.update_node(x)
            if node.right.left is not None and node.right.left.color != NIL:
                node.right.left.update_node(x)
        right_node = node.right
        left_node = right_node.left
        if left_node == self.NIL_LEAF:
            return right_node
        while left_node.left != self.NIL_LEAF:
            if x is not None:
                left_node.left.update_node(x)
            left_node = left_node.left
        return left_node

    def _get_sibling(self, node):
        parent = node.parent
        if node.key > parent.key or abs(node.key - parent.key) < Precision.EPSILON:
            sibling = parent.left
            direction = 'L'
        else:
            sibling = parent.right
            direction = 'R'
        return sibling, direction

    def find_node(self, key, x=None):
        if x is not None and abs(key - self.root.key) > Precision.EPSILON:
            self.root.update_node(x)

        def inner_find(root):
            if root is None or root == self.NIL_LEAF:
                return None

            if x is not None:
                if root.left.color != NIL:
                    root.left.update_node(x)
                if root.right.color != NIL:
                    root.right.update_node(x)

            if abs(key - root.key) < Precision.EPSILON:
                return root
            elif key > root.key:
                return inner_find(root.right)
            elif key < root.key:
                return inner_find(root.left)

        return inner_find(self.root)

    def in_order(self):
        if self.root is None:
            print('None')
            return
        self.root.in_order()

    def _find_min(self, node):
        while node.left != self.NIL_LEAF:
            node = node.left
        return node

    def _find_max(self, node):
        while node.right != self.NIL_LEAF:
            node = node.right
        return node

    def successor(self, node):
        if node.right is not self.NIL_LEAF:
            return self._find_min(node.right)
        parent = node.parent
        while parent is not None:
            if node != parent.right:
                break
            node = parent
            parent = parent.parent
        return parent

    def predecessor(self, node):
        if node.left is not self.NIL_LEAF:
            return self._find_max(node.left)
        parent = node.parent
        while parent is not None:
            if node != parent.left:
                break
            node = parent
            parent = parent.parent
        return parent
