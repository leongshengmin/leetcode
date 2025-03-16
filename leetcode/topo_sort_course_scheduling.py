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


# redo
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # we can finish if there's a topological ordering of courses
        # ie we topological ordering size = # of courses
        # and there exists a course without prerequisites

        indegrees = [0 for _ in range(numCourses)]
        adj_list = [[] for _ in range(numCourses)]

        for u, v in prerequisites:
            # u->v meaning indegree of v should be incremented
            indegrees[v] += 1
            adj_list[u].append(v)

        # there should exist a course with indegree 0 otherwise there isnt a valid ordering
        to_visit = []
        for i in range(numCourses):
            if indegrees[i] == 0:
                to_visit.append((0, i))
        if not to_visit:
            return False

        heapq.heapify(to_visit)

        while to_visit:
            indeg, u = heapq.heappop(to_visit)
            for v in adj_list[u]:
                indegrees[v] -= 1
                if indegrees[v] == 0:
                    heapq.heappush(to_visit, (0, v))

        has_gt_zero = any([d for d in indegrees if d > 0])
        if has_gt_zero:
            return False
        return True


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # can finish if there exists a topo ordering of courses
        # ie there exists >= 1 course with 0 indegree
        # we always visit the 0 indegree vertex first (using minheap) and
        # reduce the counter of indegree for vertices this vertex has an outgoing edge to

        # if we pop the minheap and we get a vertex with indegree >0 that isn't yet visited --> not possible
        # otherwise possible

        adj_list = [[] for _ in range(numCourses)]
        indegree_count = [0 for _ in range(numCourses)]

        # prerequisites [a,b] means b -> a
        # form adj_list and update indegree count here
        for u, v in prerequisites:
            indegree_count[v] += 1
            adj_list[u].append(v)

        courses = deque([i for i in range(numCourses) if indegree_count[i] == 0])

        # no vertices have indegree 0
        if not courses:
            return False

        while courses:
            u = courses.popleft()
            # visit neighbours and decrement indegree count
            # only adding them to courses we can satisfy once indegree == 0 ie no remaining prerequisites
            for v in adj_list[u]:
                indegree_count[v] -= 1
                if indegree_count[v] == 0:
                    courses.append(v)

        has_non_zero_indeg = any(i for i in indegree_count if i > 0)
        if has_non_zero_indeg:
            return False
        return True
