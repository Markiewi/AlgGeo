BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'


class TreeNode:
    epsilon = 10 ** (-10)

    def __init__(self, segment, color, parent, left=None, right=None, bottom_segment=None):
        self.key = segment.key if segment is not None else None
        self.segment = segment
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right
        self.bottom_segment = bottom_segment

    def __repr__(self):
        if self.parent is not None:
            parent = str(self.parent.segment)
            parent_side = 'Left' if self.parent.left.segment == self.segment else 'Right'
        else:
            parent = 'None'
            parent_side = ''
        bottom_segment = str(self.bottom_segment) if self.bottom_segment is not None else 'None'
        return 'key: ' + str(self.key) + ' Segment: ' + str(self.segment) + \
               ' Bottom segment: ' + bottom_segment + ' Color: ' + self.color + \
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
            parents_are_same = abs(self.parent.key - other.parent.key) < self.epsilon \
                               and self.parent.color == other.parent.color
        return (other.key is not None or (other.key is None and self.key is None)) and \
            abs(self.key - other.key) < self.epsilon and self.color == other.color and parents_are_same

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

    def print_tree(self):
        if self is None or self.color == NIL:
            return
        if self.left.color != NIL:
            self.left.print_tree()
        print('N: ', self)
        if self.right.color != NIL:
            self.right.print_tree()


class RedBlackTree:
    NIL_LEAF = TreeNode(segment=None, color=NIL, parent=None)
    epsilon = 10 ** (-10)

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

    def delete(self, segment, x=None):
        if x is not None:
            segment.key = segment.update_key(x)
        key = segment.key
        node_to_remove = self.find_node(key, x)
        # print('node_to_remove: ', node_to_remove, ' x: ', x)
        # self.in_order()
        # print('<<<<<<<<<<<>>>>>>>>>>>>>>')
        if node_to_remove.bottom_segment is not None:
            if node_to_remove.bottom_segment != segment:
                node_to_remove.segment = node_to_remove.bottom_segment

            node_to_remove.bottom_segment = None
            return

        if node_to_remove is None:
            return
        if node_to_remove.get_children_count() == 2:
            successor = self._find_in_order_successor(node_to_remove)
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
        """
        Case 1 is when there's a double black node on the root
        Because we're at the root, we can simply remove it
        and reduce the black height of the whole tree.
            __|10B|__                  __10B__
           /         \      ==>       /       \
          9B         20B            9B        20B
        """
        if self.root == node:
            node.color = BLACK
            return
        self.__case_2(node)

    def __case_2(self, node):
        """
        Case 2 applies when
            the parent is BLACK
            the sibling is RED
            the sibling's children are BLACK or NIL
        It takes the sibling and rotates it
                         40B                                              60B
                        /   \       --CASE 2 ROTATE-->                   /   \
                    |20B|   60R       LEFT ROTATE                      40R   80B
    DBL BLACK IS 20----^   /   \      SIBLING 60R                     /   \
                         50B    80B                                |20B|  50B
            (if the sibling's direction was left of it's parent, we would RIGHT ROTATE it)
        Now the original node's parent is RED
        and we can apply case 4 or case 6
        """
        parent = node.parent
        sibling, direction = self._get_sibling(node)
        if sibling.color == RED and parent.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=parent)
            parent.color = RED
            sibling.color = BLACK
            return self.__case_1(node)
        self.__case_3(node)

    def __case_3(self, node):
        """
        Case 3 deletion is when:
            the parent is BLACK
            the sibling is BLACK
            the sibling's children are BLACK
        Then, we make the sibling red and
        pass the double black node upwards
                            Parent is black
               ___50B___    Sibling is black                       ___50B___
              /         \   Sibling's children are black          /         \
           30B          80B        CASE 3                       30B        |80B|  Continue with other cases
          /   \        /   \        ==>                        /  \        /   \
        20B   35R    70B   |90B|<---REMOVE                   20B  35R     70R   X
              /  \                                               /   \
            34B   37B                                          34B   37B
        """
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
        """
        If the parent is red and the sibling is black with no red children,
        simply swap their colors
        DB-Double Black
                __10R__                   __10B__        The black height of the left subtree has been incremented
               /       \                 /       \       And the one below stays the same
             DB        15B      ===>    X        15R     No consequences, we're done!
                      /   \                     /   \
                    12B   17B                 12B   17B
        """
        parent = node.parent
        if parent.color == RED:
            sibling, direction = self._get_sibling(node)
            if sibling.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
                parent.color, sibling.color = sibling.color, parent.color  # switch colors
                return  # Terminating
        self.__case_5(node)

    def __case_5(self, node):
        """
        Case 5 is a rotation that changes the circumstances so that we can do a case 6
        If the closer node is red and the outer BLACK or NIL, we do a left/right rotation, depending on the orientation
        This will showcase when the CLOSER NODE's direction is RIGHT
              ___50B___                                                    __50B__
             /         \                                                  /       \
           30B        |80B|  <-- Double black                           35B      |80B|        Case 6 is now
          /  \        /   \      Closer node is red (35R)              /   \      /           applicable here,
        20B  35R     70R   X     Outer is black (20B)               30R    37B  70R           so we redirect the node
            /   \                So we do a LEFT ROTATION          /   \                      to it :)
          34B  37B               on 35R (closer node)           20B   34B
        """
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
        """
        Case 6 requires
            SIBLING to be BLACK
            OUTER NODE to be RED
        Then, does a right/left rotation on the sibling
        This will showcase when the SIBLING's direction is LEFT
                            Double Black
                    __50B__       |                               __35B__
                   /       \      |                              /       \
      SIBLING--> 35B      |80B| <-                             30R       50R
                /   \      /                                  /   \     /   \
             30R    37B  70R   Outer node is RED            20B   34B 37B    80B
            /   \              Closer node doesn't                           /
         20B   34B                 matter                                   70R
                               Parent doesn't
                                   matter
                               So we do a right rotation on 35B!
        """
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

    def _find_parent(self, key, x=None):
        def inner_find(parent):
            if x is not None:
                parent.segment.key = parent.segment.update_key(x)
                parent.key = parent.segment.key
                if parent.bottom_segment is not None:
                    parent.bottom_segment.key = parent.bottom_segment.update_key(x)

            if abs(key - parent.key) < self.epsilon:
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

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def find_node(self, key, x=None):
        print(key)

        if x is not None:
            if self.root.bottom_segment is not None:
                tmp = self.root.segment
                self.delete(self.root.segment)
                self.insert(tmp)
                self.root.bottom_segment.key = self.root.bottom_segment.update_key(x)
            self.root.segment.key = self.root.segment.update_key(x)
            self.root.key = self.root.segment.key

        def inner_find(root):
            print(root.key, key, x)
            if root is None or root == self.NIL_LEAF:
                return None
            if root.left.color != NIL: print(root.left.key)
            if abs(key - root.key) < self.epsilon:
                print(root)
                return root
            else:
                if root.left.color != NIL:
                    if root.left.bottom_segment is not None:
                        tmpp = root.left.segment
                        root.left.bottom_segment.key = root.left.key
                    root.left.segment.key = root.left.segment.update_key(x)
                    root.left.key = root.left.segment.key
                if root.right.color != NIL:
                    if root.right.bottom_segment is not None:
                        tmpp = root.segment
                        root.right.bottom_segment.key = root.right.key
                    root.right.segment.key = root.right.segment.update_key(x)
                    root.right.key = root.right.segment.key

                if key > root.key:
                    return inner_find(root.right)
                elif key < root.key:
                    return inner_find(root.left)

        found_node = inner_find(self.root)
        return found_node

    def _find_in_order_successor(self, node):
        right_node = node.right
        left_node = right_node.left
        if left_node == self.NIL_LEAF:
            return right_node
        while left_node.left != self.NIL_LEAF:
            left_node = left_node.left
        return left_node

    def _get_sibling(self, node):
        """
        Returns the sibling of the node, as well as the side it is on
        e.g
            20 (A)
           /     \
        15(B)    25(C)
        _get_sibling(25(C)) => 15(B), 'R'
        """
        parent = node.parent
        if node.key >= parent.key:
            sibling = parent.left
            direction = 'L'
        else:
            sibling = parent.right
            direction = 'R'
        return sibling, direction

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
