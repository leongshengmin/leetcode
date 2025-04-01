# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def lowestCommonAncestor2(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        # since this is a bst we know that right > root && left < root
        # if p < root --> p is in left subtree; if q > root --> q is in right subtree
        # if p, q in diff subtrees, then root is the lca
        # if p, q in same subtree then the larger of p, q is the lca
        def find_lca(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
            if not root:
                return None
            if p.val < root.val and q.val < root.val:
                # left subtree
                return find_lca(root.left, p, q)
            elif p.val > root.val and q.val > root.val:
                # right subtree
                return find_lca(root.right, p, q)
            # different subtrees so root is lca
            return root

        return find_lca(root, p, q)

    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        # use parent pointers to find lca
        # we iterate parent links of p to q from the end (ie p / q) and terminate once we find a common parent node
        # we find parents by iterating the tree and storing the previous node we came from

        parents = {}

        def find_parent(curr: TreeNode, parent: TreeNode, v: TreeNode):
            if not curr:
                return None
            if parent:
                print(f"setting {curr.val} {curr} to {parent.val} {parent}")
                parents[curr] = parent
            if v == curr:
                return curr
            if curr.val < v.val:
                # right subtree
                return find_parent(curr.right, curr, v)
            return find_parent(curr.left, curr, v)

        find_parent(root, None, p)
        find_parent(root, None, q)

        lca = None
        while p and q:
            if p == q:
                lca = p
                break
            p = parents.get(p)
            q = parents.get(q)
        return lca
