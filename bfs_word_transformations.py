from collections import deque
from typing import List


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # model each word in word list as a graph node
        # edge determines reachability from current beginWord state to the other word nodes
        # we have an edge if it's possible to tx from beginWord to some other word
        
        visited = set()
        to_visit = deque()
        min_word_len = len(beginWord) - 1
        
        def bfs(begin: str, end: str, word_list: List[str]) -> int:
            to_visit.append((begin, 0))

            while to_visit:
                curr, hops = to_visit.popleft()
                visited.add(curr)

                if curr == end:
                    return hops+1
                
                # add neighbours 1 hop away, skipping words we've already visited
                for word in word_list:
                    if word in visited:
                        continue
                    
                    # check if word is transformable
                    num_diff_chars = 0
                    for i in range(len(word)):
                        if num_diff_chars > 1:
                            break
                        wi = word[i]
                        ci = curr[i]
                        if wi != ci:
                            num_diff_chars += 1

                    if num_diff_chars > 1:
                        continue

                    to_visit.append((word, hops+1))

            return 0
        
        if not wordList:
            return 0
        
        return bfs(beginWord, endWord, wordList)

beginWord="talk"
endWord="tail"
wordList=["talk","tons","fall","tail","gale","hall","negs"]
print(Solution().ladderLength(beginWord, endWord, wordList))
