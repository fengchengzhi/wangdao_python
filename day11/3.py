import random


class TreeNode:
    def __init__(self, val=-1, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Tree:

    def __init__(self):
        self.root = None
        self.queue = []

    def tree_insert(self, val):
        p1 = TreeNode(val)
        self.queue.append(p1)
        if not self.root:
            self.root = p1
        else:
            if not self.queue[0].left:
                self.queue[0].left = p1
            elif not self.queue[0].right:
                self.queue[0].right = p1
                self.queue.pop(0)
            else:
                print('wrong')

    def preorder(self):
        st1 = []
        p = self.root
        while st1 or p:
            while p:
                print(p.val, end=' ')
                st1.append(p)
                p = p.left
            p = st1.pop()
            p = p.right

    def midorder(self):
        st1 = []
        p = self.root
        while st1 or p:
            while p:
                st1.append(p)
                p = p.left
            p = st1.pop()
            print(p.val, end=' ')
            p = p.right

    def postorder(self, root):
        if not root:
            return
        self.postorder(root.left)
        self.postorder(root.right)
        print(root.val, end=' ')

    def cengxu(self):
        q1 = [self.root]
        while q1:
            p1 = q1.pop(0)
            if p1:
                print(p1.val, end=' ')
                if p1.left:
                    q1.append(p1.left)
                if p1.right:
                    q1.append(p1.right)


if __name__ == '__main__':
    tree = Tree()
    for i in range(10):
        tree.tree_insert(random.randint(0, 20))
    tree.cengxu()
    print()
    tree.preorder()
    print()
    tree.midorder()
    print()
    tree.postorder(tree.root)
