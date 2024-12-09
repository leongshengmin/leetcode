class Solution:
    def isNStraightHand(self, hand: list[int], groupSize: int) -> bool:
        # starting from min item in hand, need to find group of group size
        # sort hand
        hand.sort()
        num_groups = int(len(hand)/groupSize)
        if len(hand)%groupSize>0:
            return False
    
        # we need to iterate num_groups times
        for _ in range(num_groups):
            curr_group_size = 0
            i = 0
            prev_in_group = -1
            while i < len(hand):
                print(f"i={i},curr_group_size={curr_group_size},prev_in_group={prev_in_group}")
                # item already taken
                if hand[i] < 0:
                    i+=1
                    continue
                
                # first item in group
                if hand[i] >= 0 and curr_group_size == 0:
                    prev_in_group = hand[i]
                    hand[i] = -1
                    curr_group_size += 1
                    i+=1
                    continue
                
                # collected enough items
                if curr_group_size >= groupSize:
                    break
                
                # look for prev_in_group + 1
                if hand[i] == prev_in_group+1:
                    # mark taken
                    prev_in_group = hand[i]
                    hand[i] = -1
                    curr_group_size += 1
                    i+=1
                    continue
                i+=1
                
            # unable to collect enough items in group
            if curr_group_size < groupSize:
                return False
        return True

hand=[1,2,4,2,3,5,3,4]
groupSize=4
print(Solution().isNStraightHand(hand, groupSize))