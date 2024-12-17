class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # return true if we can create a topological ordering of courses
        #
        # maintain indegree array
        # each time we pop the vertex with indegree 0
        # iterate through the neighbors, decreasing the indegree count for them
        # and then adding them to the min heap
        #
        # if we manage to pop all the vertices (ie all have 0 indegree eventually), we have a topo ordering --> true
        # otherwise --> return false
        #
        # prereqs [a,b] means edge b->a

        adj_list = [[] for _ in range(numCourses)]
        indegree = [0 for _ in range(numCourses)]
        for v, u in prerequisites:
            # u->v
            indegree[v] = indegree[v] + 1
            adj_list[u].append(v)

        # add vertices to minheap
        # weight will be indegree so that we always pop vertex with min indegree
        tovisit = deque()

        # there should be a course with no prereq otherwise we wont be able to fulfil
        for i in range(numCourses):
            if indegree[i] == 0:
                tovisit.append(i)

        if not tovisit:
            return False

        courses_left = numCourses
        while tovisit:
            u = tovisit.popleft()
            courses_left -= 1
            for v in adj_list[u]:
                indegree[v] = indegree[v] - 1
                if indegree[v] == 0:
                    tovisit.append(v)
        if courses_left > 0:
            return False
        return True


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # return true if we can create a topological ordering of courses
        #
        # maintain indegree array
        # each time we pop the vertex with indegree 0
        # iterate through the neighbors, decreasing the indegree count for them
        # and then adding them to the min heap
        #
        # if we manage to pop all the vertices (ie all have 0 indegree eventually), we have a topo ordering --> true
        # otherwise --> return false
        #
        # prereqs [a,b] means edge b->a

        adj_list = [[] for _ in range(numCourses)]
        indegree = [0 for _ in range(numCourses)]
        for v, u in prerequisites:
            # u->v
            indegree[v] = indegree[v] + 1
            adj_list[u].append(v)

        # add vertices to minheap
        # weight will be indegree so that we always pop vertex with min indegree
        tovisit = deque()

        # there should be a course with no prereq otherwise we wont be able to fulfil
        for i in range(numCourses):
            if indegree[i] == 0:
                tovisit.append(i)

        if not tovisit:
            return []

        ordering = []
        while tovisit:
            u = tovisit.popleft()
            ordering.append(u)
            for v in adj_list[u]:
                indegree[v] = indegree[v] - 1
                if indegree[v] == 0:
                    tovisit.append(v)
        if len(ordering) < numCourses:
            return []
        return ordering
