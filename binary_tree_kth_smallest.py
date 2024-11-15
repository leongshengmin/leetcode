# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        def count_nodes(root:Optional[TreeNode]) -> int:
            if not root:
                return 0
            return 1 + count_nodes(root.left) + count_nodes(root.right)

        # find number of nodes in left subtree
        # if < k-1 then we need to explore right subtree as well
        # if == k-1 then current root node is the kth elem
        # if > k then answer is in left subtree
        # set either left / right child as root and cont exploring
        if not root:
            return -1
        l = count_nodes(root.left)
        if l+1 == k:
            return root.val
        elif l+1 < k:
            return self.kthSmallest(root.right, k-l-1)
        return self.kthSmallest(root.left, k)
        