# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # need to check that all nodes in left < curr node
        # and all nodes in right > curr node
        # not just local view of immd left, right children
        def is_valid(root: Optional[TreeNode], leftval: float, rightval: float) -> bool:
            if not root:
                return True
            if not (root.val > leftval and root.val < rightval):
                return False

            # left child should be smaller than current
            # and right right should be larger than current
            return is_valid(root.left, leftval, root.val) and is_valid(
                root.right, root.val, rightval
            )

        return is_valid(root, float("-inf"), float("inf"))
