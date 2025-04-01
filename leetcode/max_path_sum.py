# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # there are >= 3 cases
        # 1. left subtree is negative so we exclude left subtree; if root is also negative we may exclude root
        # 2. right subtree is negative so we exclude right
        # 3. left, right subtree + root positive so we include all
        def get_path_sum(root: Optional[TreeNode]) -> int:
            if not root:
                return 0

            left_path = get_path_sum(root.left)
            right_path = get_path_sum(root.right)
            take_left_path = max(left_path, 0)
            take_right_path = max(right_path, 0)
            res = max(
                max(take_left_path + root.val + take_right_path, take_left_path),
                take_right_path,
            )
            return res

        return get_path_sum(root)
