class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # try each start position
        # initial tankvol = 0
        # get next index (i+1)%len(gas). At each station that isnt start calculate tankvol += tankvol - cost[i] + gas[nextidx]
        # if we manage to cover all i then return true
        # otherwise if tankvol <= 0 before we reach destination return False
        memo = {}
        def helper(start_idx:int, end_idx: int, gas:List[int], cost:List[int], tank_vol:int, initial:bool=False) -> bool:
            """helper method that checks from start index {idx} the tankvol remaining after going to the next station.
            """
            if start_idx == end_idx and not initial:
                return True
            
            if (start_idx,end_idx,tank_vol) in memo:
                return memo[(start_idx,end_idx,tank_vol)]

            next_idx = (start_idx+1)%len(gas)
            tank_vol_to_travel = tank_vol - cost[start_idx]
            if tank_vol_to_travel < 0:
                return False

            new_tank_vol = tank_vol_to_travel + gas[next_idx]
            res = helper(next_idx, end_idx, gas, cost, new_tank_vol, initial=False)
            memo[(start_idx,end_idx,tank_vol)] = res
            return res
        
        for i in range(len(gas)):
            res = helper(i, i, gas, cost, gas[i], initial=True)
            if not res:
                continue
            return i
        return -1
