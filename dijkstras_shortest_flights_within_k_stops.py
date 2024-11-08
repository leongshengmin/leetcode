"""
There are n cities connected by some number of flights.
You are given an array flights where flights[i] = [fromi, toi, pricei]
indicates that there is a flight from city fromi to city toi with cost pricei.

You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.


since this is a directed graph and they want to find shortest path from arbitrary src vertex to dst vertex,
use dijkstras (shortest path algo).
we need to modify dijkstras here due to limitation of k hops
since path with >k hops may be more optimal but shouldnt be valid here.
at each step also record the number of hops from src to arbitrary vertex v. 
"""