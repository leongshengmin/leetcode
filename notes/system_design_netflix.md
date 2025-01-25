![overview](https://media.licdn.com/dms/image/v2/C5112AQHVt9yrq8Br1Q/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1535206730604?e=1741824000&v=beta&t=pUL1LS1b1bZnRkc3NrykkRRYyk2EC2R52JAnVqjIS7o)

openconnect CDN

**proxy (ZUUL netty server)**
The Netty handlers on the front and back of the filters are mainly responsible for handling the network protocol, web server, connection management and proxying work. With those inner workings abstracted away, the filters do all of the heavy lifting.

The inbound filters run before proxying the request and can be used for authentication, routing, or decorating the request.

The endpoint filters can either be used to return a static response or proxy the request to the backend service (or origin as we call it).

The outbound filters run after a response has been returned and can be used for things like gzipping, metrics, or adding/removing custom headers.

Features:

    Supports http2
    mutual TLS
    Adaptive retries
    Concorrency protection for origin

It helps in Easy routing based on query params, url, path. The main use case is for routing traffic to a specific test or staging cluster.

Advantages: ??

    Services needing to shard their traffic create routing rules that map certain paths or prefixes to separate origins
    Developers onboard new services by creating a route that maps a new hostname to their new origin
    Developers run load tests by routing a percentage of existing traffic to a small cluster and ensuring applications will degrade gracefully under load
    Teams refactoring applications migrate to a new origin slowly by creating rules mapping traffic gradually, one path at a time
    Teams test changes (canary testing) by sending a small percentage of traffic to an instrumented cluster running the new build
    If teams need to test changes requiring multiple consecutive requests on their new build, they run sticky canary tests that route the same users to their new build for brief periods of time
    Security teams create rules that reject “bad” requests based on path or header rules across all Zuul clusters

**hystrix (circuit breakers when connecting to upstreams)**
Hystrix is a latency and fault tolerance library designed to isolate points of access to remote systems, services and 3rd party libraries. which helps in

    Stop cascading failures
    Realtime monitoring of configurations changes
    Concurrency aware request caching
    Automated batching through request collapsing

IE. If a micro service is failing then return the default response and wait until it recovers.

**Caching (Hot:EVCache on Memcached using RAM; Cold: SSD)**
EVCache:

When a node goes down all the cache goes down along with it. so performace hit until all the data is cached. so what netflix did is they came up with EVcache. It is wrapper around Memcached but it is sharded so multiple copies of cache is stored in sharded nodes. So everytime the write happens, all the shards are updated too..

When cache reads happens, read from nearest cache or nodes, but when a node is not available, read from different available node. It handles 30 million request a day and linear scalability with milliseconds latency.

SSDs for Caching:

Storing large amounts of data in volatile memory (RAM) is expensive. Modern disk technologies based on SSD are providing fast access to data but at a much lower cost when compared to RAM. Hence, we wanted to move part of the data out of memory without sacrificing availability or performance. The cost to store 1 TB of data on SSD is much lower than storing the same amount in RAM.

**SQL Database (mysql)**
Writes:
master-master setup with “Synchronous replication protocol” is used to replicate write operations from the primary master node to the secondary master node. Only after both the local and remote writes have been confirmed does the write succeed. This ensures data between both master nodes are kept in-sync. Loss of a single node is guaranteed to have no data loss. This increases the write latency but we get increased resiliency.

In case of the primary MySQL database failure, a failover is performed to the secondary node that was being replicated in synchronous mode. Once secondary node takes over the primary role, the route53 DNS entry for database host is changed to point to the new primary.

Reads:
Reads can be served by any read replica node but will be routed to the node that is closest to the client.
The read traffic from ETL jobs was diverted to the read replica, sparing the primary database from heavy ETL batch processing.

**nosql database (cassandra)**

Cassandra is a distributed wide column store NoSQL database designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure (similar to clickhouse ie columnar store + nosql).

At Netflix as userbase started to grow more there has been a massive increase in viewing history data. So Netflix Redesigned data storage arch with two main goals in mind:
- Smaller Storage Footprint.
- Consistent Read/Write Performance as viewing per member grows.

So the solution: Compress the old rows!! Data was divided in to two types
- Live Viewing History (LiveVH): Small number of recent viewing records with frequent updates. The data is stored in uncompressed form as in the simple design detailed above.
- Compressed Viewing History (CompressedVH): Large number of older viewing records with rare updates. The data is compressed to reduce storage footprint. Compressed viewing history is stored in a single column per row key.

