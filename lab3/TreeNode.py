# the nodes of the broom's structure root, each node holds 7 attributes
# segment - line segment so we know where is lies in the top - bottom order
# key - simply coordinate y of the first point of the line segment
# top - the top neighbour of the line segment in the current position of the broom
# bottom - same as top but it's the bottom neighbour
# and three regular attributes of binary search tree - left, right and parent


class TreeNode:
    def __init__(self, segment):
        self.segment = segment
        self.key = segment.p.y
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        if self is None:
            return 'None'

        if self.top is not None:
            t = ' top: ' + str(self.top.segment)
        else:
            t = ' top: None'
        if self.bottom is not None:
            b = ' bottom: ' + str(self.bottom.segment)
        else:
            b = ' bottom: None'

        return 'Segment: ' + str(self.segment) + t + b

    def delete(self, segment):
        node = self.find(segment)

        if node.top is not None:
            node.top.bottom = node.bottom
        if node.bottom is not None:
            node.bottom.top = node.top

        return self.delete_inner(segment)

    def delete_inner(self, segment):
        key = segment.p.y
        if self.segment == segment:
            if self.right and self.left:
                [psucc, succ] = self.right.delete_find_min(self)

                if psucc.left == succ:
                    psucc.left = succ.right
                else:
                    psucc.right = succ.right

                succ.left = self.left
                succ.right = self.right

                return succ
            else:
                if self.left:
                    return self.left
                else:
                    return self.right
        else:
            if self.key > key:
                if self.left:
                    self.left = self.left.delete_inner(segment)

            else:
                if self.right:
                    self.right = self.right.delete_inner(segment)

        return self

    def delete_find_min(self, parent):
        if self.left:
            return self.left.delete_find_min(self)
        else:
            return [parent, self]

    def intersection(self, segment1, segment2):
        node1 = self.find(segment1)
        node2 = self.find(segment2)

        if node1.bottom == node2:
            tmp = node1
            node1 = node2
            node2 = tmp

        if node1.bottom is not None:
            node1.bottom.top = node2
        if node2.top is not None:
            node2.top.bottom = node1
        node1.top = node2.top
        node2.bottom = node1.bottom
        node1.bottom = node2
        node2.top = node1

    def insert(self, segment, x):
        key = segment.p.y

        if key <= self.key:
            if self.left:
                self.left.insert(segment, x)
            else:
                self.left = TreeNode(segment)
                self.left.parent = self
                self.left.neighbours(x)
        else:
            if self.right:
                self.right.insert(segment, x)
            else:
                self.right = TreeNode(segment)
                self.right.parent = self

                self.right.neighbours(x)

    def neighbours(self, x):
        succ = self.successor(self.segment)
        pred = self.predecessor(self.segment)

        height = self.current_height(x)

        if succ is None and pred is None:
            return [None, None]

        if succ is not None and succ.current_height(x) > height:
            while succ.bottom is not None and succ.bottom.current_height(x) > height:
                succ = succ.bottom
        elif succ is not None and succ.current_height(x) < height:
            while succ.top is not None and succ.top.current_height(x) < height:
                succ = succ.top

        if pred is not None and pred.current_height(x) > height:
            while pred.bottom is not None and pred.bottom.current_height(x) > height:
                pred = pred.bottom
        elif pred is not None and pred.current_height(x) < height:
            while pred.top is not None and pred.top.current_height(x) < height:
                pred = pred.top

        if succ is not None:
            self.top = succ
            succ.bottom = self
        if pred is not None:
            self.bottom = pred
            pred.top = self

    def successor(self, segment):
        temp = self.find(segment)
        if temp.right is not None:
            return temp.right.find_min()
        parent = temp.parent
        child = temp
        while parent is not None and child is parent.right:
            child = parent
            parent = child.parent
        return parent

    def predecessor(self, segment):
        temp = self.find(segment)
        if temp.left is not None:
            return temp.find_max()
        parent = temp.parent
        child = temp
        while parent is not None and child is parent.left:
            child = parent
            parent = child.parent
        return parent

    def find(self, segment):
        key = segment.p.y
        if self is None:
            return None
        elif self.segment == segment:
            return self
        elif key <= self.key:
            return self.left.find(segment)
        else:
            return self.right.find(segment)

    def find_min(self):
        if self.left is not None:
            return self.left.find_min()
        else:
            return self

    def find_max(self):
        if self.right is not None:
            return self.right.find_max()
        else:
            return self

    def current_height(self, x):
        a = self.segment.calculate_slope()
        b = self.segment.calculate_y_intersect()
        return a * x + b

    def in_order(self):
        if self.left is not None:
            self.left.in_order()
        print(self)
        if self.right is not None:
            self.right.in_order()

    def check_parents(self):
        if self.left is not None:
            self.left.check_parents()
        if self.parent is None:
            print('root')
        else:
            if self.parent.left == self:
                print('lewe dziecko')
            elif self.parent.right == self:
                print('prawe dziecko')
        if self.right is not None:
            self.right.check_parents()
