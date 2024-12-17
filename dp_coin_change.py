# TODO: fix this dp wrong
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # for each coin we either take or not
        # take=advance coin ptr, decrement amount
        # donttake=advance coin ptr, same amount

        # memoize using coin_idx, amount_left
        # ie len(coins) * amount grid
        memo = [[0 for _ in range(amount + 1)] for _ in range(len(coins))]

        def helper(coin_idx, coins, amount_left, num_coins) -> int:
            if amount_left == 0:
                return num_coins
            if coin_idx >= len(coins):
                return 999999999

            if memo[coin_idx][amount_left] != 0:
                return memo[coin_idx][amount_left]

            # max coins for this denom we can take
            coin_val = coins[coin_idx]
            max_coins = int(amount_left / coin_val)
            # we can take 0..max_coins (inclusive)
            res = min(
                [
                    helper(
                        coin_idx + 1, coins, amount_left - (coin_val * i), num_coins + i
                    )
                    for i in range(max_coins + 1)
                ]
            )
            memo[coin_idx][amount_left] = res
            return res

        min_coins = helper(0, coins, amount, 0)
        if min_coins == 999999999:
            return -1
        return min_coins
