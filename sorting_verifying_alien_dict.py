class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        # convert each word into its numerical equivalent using order then sort result
        # if ordering in sorted == words ordering --> True
        # otherwise false
        #
        # e.g. w1=abc; w2 = adc
        # w1's numerical value for sorting = sum of all i_s {order.find(w1[i]) * 10^((len(w1)-1) - i)}

        def get_numeric_equivalent(word: str, order: str) -> int:
            res = 0
            word_len = len(word)
            for i in range(word_len):
                idx = order.find(word[i])
                if idx == -1:
                    idx = 0
                res_i = idx * 10 ** ((word_len - 1) - i)
                res += res_i
            return res

        word_to_number_map = {
            word: get_numeric_equivalent(word, order) for word in words
        }

        # sort dict by value
        word_to_number_map = {
            k: v
            for k, v in sorted(word_to_number_map.items(), key=lambda item: item[1])
        }

        # check if order is the same
        sorted_keys = set(word_to_number_map.keys())
        return set(words) == set(sorted_keys)
