"""
Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

 

Example 1:

Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]

Example 2:

Input: preorder = [-1], inorder = [-1]
Output: [-1]
"""
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import List, Optional


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # iterate preorder
        # inorder defines for a given node v, what should be on the left, right subtree
        # for each item in preorder, find the index in inorder
        # if left of inorder val is single item that's the leaf
        if not preorder:
            return None
        if not inorder:
            return None
        
        # at each step of the recursion we pop the first item in preorder as that's the root
        # NOTE: preorder[1:] does NOT work since original references to the list does not change
        # NOTE: need to use preorder.pop(0) instead as that modifies the list bound to preorder
        # preval = preorder[0]
        preval = preorder.pop(0)
        inidx = inorder.index(preval)
        left = inorder[:inidx]
        right = inorder[inidx+1:]
        curr = TreeNode(val=preval)
        curr.left = self.buildTree(preorder,left)
        curr.right = self.buildTree(preorder, right)
        return curr

