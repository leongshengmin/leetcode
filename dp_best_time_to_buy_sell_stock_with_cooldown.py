class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        
        memo={}
        def helper(prices:List[int], i:int, is_buy:bool) -> int:
            if i>=len(prices):
                return 0
            
            if (is_buy, i) in memo:
                return memo[(is_buy, i)]
            
            # have to buy now or eventually
            later = helper(prices, i+1, is_buy)
            if is_buy:
                buy_now = helper(prices, i+1, not is_buy)-prices[i]
                memo[(is_buy, i)] = max(buy_now, later)

            else:            
                # otherwise we have coins
                # can sell now or later
                sell_now = helper(prices, i+2, not is_buy)+prices[i]
                memo[(is_buy, i)] = max(sell_now, later)
            return memo[(is_buy, i)]
        
        return helper(prices, 0, True)
