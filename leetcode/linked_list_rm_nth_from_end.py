# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # keep counter of pos from start
        # also maintain prev, curr ptr for joining list

        # iterate once through linked list to check which node to rm
        curr = head
        num_nodes = 0
        while curr:
            num_nodes += 1
            curr = curr.next

        index_from_start = num_nodes - n

        # edge case when n is the head
        if index_from_start <= 0:
            head = head.next
            return head

        curr = head
        prev = None
        cnt = 0
        while curr:
            if cnt == index_from_start:
                prev.next = curr.next
                break
            prev = curr
            curr = curr.next
            cnt += 1
        return head
