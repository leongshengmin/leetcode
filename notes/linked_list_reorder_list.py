# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        # have 2 ptrs -- 1 at head, 1 at tail
        # advance head then tail
        # tmp = head.next
        # curr = head
        # curr.next = tail
        # head = tmp
        # tmp = tail.next
        # curr = tail
        # curr.next = head
        # tail = tmp
        arr = []
        curr = head
        while curr:
            arr.append(curr)
            curr = curr.next

        curr = head
        for i in range(1, len(arr)):
            tmpnext = None
            if i%2==0:  # i = i/2
                tmpnext = arr[int(i/2)]
            else:   # i = n-((i+1)/2)
                tmpnext = arr[len(arr)-int((i+1)/2)]
            curr.next = tmpnext

            if i>=len(arr)-1:
                tmpnext.next = None
                continue
            curr = curr.next
