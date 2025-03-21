# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

import math
from typing import List, Optional


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # each level max has 2^(level) nodes. Where level is 0-indexed
        # if node has no children then append None,None
        # at the end rm the Nones from the res
        res = []
        if not root:
            return res

        to_visit = deque([root])

        while to_visit:
            qlen = len(to_visit)
            level = []
            # number of nodes in this level
            for i in range(qlen):
                # each level we go to we enqueue all the children of nodes from this level
                curr = to_visit.popleft()
                # ignore curr if its empty
                if not curr:
                    continue
                level.append(curr.val)
                to_visit.append(curr.left)
                to_visit.append(curr.right)
            if not level:
                continue
            res.append(level)

        return res


# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # for each level we need to store the nodes in an array to visit them in order
        if not root:
            return []

        res = []
        to_visit = deque([[root]])
        while to_visit:
            prev_level_nodes = to_visit.popleft()
            print(prev_level_nodes)
            res.append([n.val for n in prev_level_nodes])
            level_nodes = []
            for node in prev_level_nodes:
                if node.left:
                    level_nodes.append(node.left)
                if node.right:
                    level_nodes.append(node.right)
            if not level_nodes:
                continue
            to_visit.append(level_nodes)
        return res
