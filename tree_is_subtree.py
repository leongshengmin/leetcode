# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def isSameTree(root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
            if not root and not subRoot:
                return True
            if root and not subRoot:
                return False
            if not root and subRoot:
                return False
            return (
                root.val == subRoot.val
                and isSameTree(root.left, subRoot.left)
                and isSameTree(root.right, subRoot.right)
            )

        # is subtree should return true if either left or right subtree is true
        # if both root, subroot empty return true
        if not subRoot:
            return True
        if not root:
            return False

        # otherwise check left OR right subtree
        return (
            isSameTree(root, subRoot)
            or self.isSubtree(root.left, subRoot)
            or self.isSubtree(root.right, subRoot)
        )
