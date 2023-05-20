RED = 0
BLACK = 1


# 左旋
def left_rotate(tree, node):
    if not node.right:
        return False
    node_r = node.right
    node_p = node.p
    node_r.p = node_p
    if not node_p:
        tree.root = node_r
    elif node_p.right == node:
        node_p.right = node_r
    else:
        node_p.left = node_r
    if node_r.left:
        node_r.left.p = node
    node.right = node_r.left
    node_r.left = node
    node.p = node_r


# 右旋
def right_rotate(tree, node):
    if not node.left:
        return False
    node_l = node.left
    node_p = node.p
    node_l.p = node_p
    if not node_p:
        tree.root = node_l
    elif node_p.left == node:
        node_p.left = node_l
    else:
        node_p.right = node_l
    if node_l.right:
        node_l.right.p = node
    node.left = node_l.right
    node_l.right = node
    node.p = node_l


# 结点
class RedBlackTreeNode:
    def __init__(self, val):
        self.val = val
        self.color = RED
        self.left = None
        self.right = None
        self.p = None


# 树
class RedBlackTree:
    def __init__(self):
        self.root: RedBlackTreeNode = None

    # 插入结点
    def insert_node(self, node: RedBlackTreeNode):
        if not self.root:
            self.root = node
            self.insert_fixup(node)
            return
        x = self.root
        while x:
            y = x
            if node.val > x.val:
                x = x.right
            else:
                x = x.left
        if y.val > node.val:
            y.left = node
        else:
            y.right = node
        node.p = y
        # 调整结点
        self.insert_fixup(node)

    # 调整结点
    def insert_fixup(self, node):
        node_p: RedBlackTreeNode = node.p
        while node_p and node_p.color == RED:
            node_g: RedBlackTreeNode = node_p.p
            if node_g.left == node_p:
                node_n: RedBlackTreeNode = node_g.right
                if node_n and node_n.color == RED:
                    node_g.color = RED
                    node_p.color = BLACK
                    node_n.color = BLACK
                    node = node_g
                    node_p = node.p
                    continue
                if node == node_p.right:
                    left_rotate(self, node_p)
                    node, node_p = node_p, node
                right_rotate(self, node_g)
                node_p.color = BLACK
                node_g.color = RED
                break
            else:
                node_n: RedBlackTreeNode = node_g.left
                if node_n and node_n.color == RED:
                    node_g.color = RED
                    node_p.color = BLACK
                    node_n.color = BLACK
                    node = node_g
                    node_p = node.p
                    continue
                if node == node_p.left:
                    right_rotate(self, node_p)
                    node, node_p = node_p, node
                left_rotate(self, node_g)
                node_p.color = BLACK
                node_g.color = RED
                break
        self.root.color = BLACK


def rbtree_print(node, key, direction):
    if node:
        if direction == 0:  # tree是根节点
            print("%2d(B) is root" % node.val)
        else:  # tree是分支节点
            print("%2d(%s) is %2d's %6s child" % (
                node.val, ("B" if node.color == 1 else "R"), key, ("right" if direction == 1 else "left")))

        rbtree_print(node.left, node.val, -1)
        rbtree_print(node.right, node.val, 1)


def main():
    number_list = (7, 4, 1, 8, 5, 2, 9, 6, 3)
    tree = RedBlackTree()
    for number in number_list:
        node = RedBlackTreeNode(number)
        tree.insert_node(node)
        del node
    rbtree_print(tree.root, tree.root.val, 0)


if __name__ == '__main__':
    main()
