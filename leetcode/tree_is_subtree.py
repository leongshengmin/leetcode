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


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        # is subtree if there exists a child wherein from that child's root isSameTree as subroot
        def isSameTree(r1: Optional[TreeNode], r2: Optional[TreeNode]) -> bool:
            if (not r1 and r2) or (not r2 and r1):
                return False
            if not r1 and not r2:
                return True
            return (
                r1.val == r2.val
                and isSameTree(r1.left, r2.left)
                and isSameTree(r1.right, r2.right)
            )

        # subroot should always be a subset of root
        if not root and subRoot:
            return False

        # if we finish checking subroot then this is a valid subtree
        if not subRoot:
            return True

        # check if this could be a subtree since root vals are the same
        if root.val == subRoot.val:
            is_same = isSameTree(root, subRoot)
            if is_same:
                return True

        # otherwise we check the left and right children of root to see if any of the children
        # are valid subtrees
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
