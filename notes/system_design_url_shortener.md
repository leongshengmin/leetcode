Core Requirements
- The system should ensure uniqueness for the short codes (no two long URLs can map to the same short URL)
- The redirection should occur with minimal delay (< 100ms)
- The system should be reliable and available 99.99% of the time (availability > consistency)
- The system should scale to support 1B shortened URLs and 100M DAU

> An important consideration in this system is the significant imbalance between read and write operations. The read-to-write ratio is heavily skewed towards reads, as users frequently access shortened URLs, while the creation of new short URLs is comparatively rare. For instance, we might see 1000 clicks (reads) for every 1 new short URL created (write). This asymmetry will significantly impact our system design, particularly in areas such as caching strategies, database choice, and overall architecture.

## API endpoints
1. POST
To shorten a URL, we’ll need a POST endpoint that takes in the long URL and expiration date, and returns the shortened URL. We use post here because we are creating a new entry in our database mapping the long url to the newly created short url.
```
// Shorten a URL
POST /urls
{
  "long_url": "https://www.example.com/some/very/long/url",
  "expiration_date": "optional_expiration_date"
}
->
{
  "short_url": "http://short.ly/abc123"
}
```

2. GET
For redirection, we’ll need a GET endpoint that takes in the short code and redirects the user to the original long URL. GET is the right verb here because we are reading the existing long url from our database based on the short code.
```
// Redirect to Original URL
GET /{short_code}
-> HTTP 302 Redirect to the original long URL
```

## Architecture

RDBMS vs NoSQL
RDBMS: hard to scale, ACID
NoSQL: eventually consistnecy

Both solution 1,2 can't use NoSQL due to acid requirement.
Solution 1:
- convert long url into short url using base62.
- store mapping of long to short url only if short url is not yet used in DB. (but this requires locking if multiple processes are involved and generate the same short url for different long urls ie higher collision)

Solution 2:
- convert long url into short url using md5 hash then get the first 7 chars.
- - store mapping of long to short url only if short url is not yet used in DB. (but this requires locking if multiple processes are involved and generate the same short url for different long urls ie but lower collision)


Solution 3:
- use global counter to get unique counter value. This prevents collisions and allows us to not need NoSQL
not good for scaling -- SPOF if single counter fails; what if counter limit exhausted;

To address scaling issues in solution 3, use ZK/dynamodb to do service discovery between the counter services. server will talk to ZK to know which redis server to talk to.

// flow
```
internet -> LB -> shortener srv -> redis counter service (for global unique id) -> nosql / rdbms (for persistence) -> once write to DB succeeds, writeback to cache (redis)
                            ----------> ZK (for redis counter srv to be alloc int range)
```

We use consistent hashing to allocate ranges to redis servers and to handle addition/removal of servers gracefully. Different from static hashing that requires no. of servers to be unchanged since server is calculated using `hash(short_url) % num_servers`.
In consistent hashing, we have a circular hash ring with `num_slots` nodes. The assigned range is determined using `total range // num_slots` (e.g. node 0 gets 0..10000, node 1 gets 10000..20000...).
Actual servers are assigned nodes using `hash(server_ip) % num_slots` then rotating clockwise to find the nearest node.
Values are then hashed to find the nearest node rotating clockwise. ie `hash(short_url) % num_slots`.
When a new server is added, we assign the new redis server a node and allocate it a new int range.
When a server is removed / healthcheck failure, the int range is freed.

To find the right redis server, the client needs to calculate which node to use using `hash(short_url) % num_slots` then rotating clockwise to find the right node.

Each redis server talks to ZK to get assigned range of counter integers e.g. (1M-2M; 2M-3M). Since each redis counter server is allocated a different range of integers to give out, no collision.
- Even if redis server goes down, will not cause SPOF just range of ints go unused.
- If new server added, new int range allocated.
- If int range exhausted in redis counter server, redis counter server can request for new range
Redis counter service will return unique counter id to the shortener srv to generate the short url before persisting this in nosql/rdbms.
In this soln we are generating a new short url each time a long url comes in if it doesnt exist in redis cache/DB. We can use a bloom filter which is a probabilistic data structure to tell if a long url exists or not. This may return false positives ie that long url exists even when it doesn't. We need to handle this case and will need to query DB for this.


![write_path_arch](https://d248djf5mc6iku.cloudfront.net/excalidraw/395831cae417d3d32f73cf7e79ee766c)
we can probably replace DB with redis if we do not have to store too much data.

// overcomplicated
1. client sends a POST request to /urls with the long url and expiration date.
2. server calculates sha256 hash of the long url (get an integer value from this hash). hash % number_of_redis_servers = which server this long url should be routed to.
This ensures that for a given long url, this will always be routed to the same redis server as long as the number of redis servers remain static.
3. Use the long_url to query redis for the short_url, expired_at.
    - if not present, then url may have been expired out of redis or new url.
    - if present, return the short url.
4. If not present in redis, use INCR op to get the next incremented counter value at `unique_counter` key.
5. Concat redis server id + `unique_counter` value that is local to the redis server. Use base62 encoding to encode short url (each base62 encoded character consumes 6 bits).
Base62 uses 62 different characters meaning less collision as compared to base10. Using 7 chars to represent short url, we get 62^7 combinations vs 10^7
6. Store generated short_url, expired_at=utc_now+ttl in redis and set ttl for the entry at long_url.

**Preventing collisions using redis**
One way to guarantee we don't have collisions is to simply increment a counter for each new url. We can then take the output of the counter and encode it using base64 encoding to ensure it's a compacted representation.
Redis is particularly well-suited for managing this counter because it's single-threaded and supports atomic operations. Being single-threaded means Redis processes one command at a time, eliminating race conditions. Its INCR command is atomic, meaning the increment operation is guaranteed to execute completely without interference from other operations. This is crucial for our counter - we need absolute certainty that each URL gets a unique number, with no duplicates or gaps.
Each counter value is unique, eliminating the risk of collisions without the need for additional checks. Incrementing a counter and encoding it is computationally efficient, supporting high throughput. With proper counter management, the system can scale horizontally to handle massive numbers of URLs. The short code can be easily decoded back to the original ID if needed, aiding in database lookups.

In a distributed environment, maintaining a single global counter can be challenging due to synchronization issues. Maybe we can shard redis and route requests that have the same long url to the same redis server or the (n+1)th server for load balancing. Routing is to ensure that for identical long urls, the translated short url is the same.
![redis](https://d248djf5mc6iku.cloudfront.net/excalidraw/7f6720321b39443d5cb96b6bdd4f26a2)

![read_path_arch](https://d248djf5mc6iku.cloudfront.net/excalidraw/8e6bc3830adfc2606d6265077d5791a6)
When a user accesses a shortened URL, the following process occurs:
- The user's browser sends a GET request to our server with the short code (e.g., GET /abc123).
- Our Primary Server receives this request and looks up the short code (abc123) in the database.
- If the short code is found and hasn't expired (by comparing the current date to the expiration date in the database), the server retrieves the corresponding long URL.
- The server then sends an HTTP redirect response to the user's browser, instructing it to navigate to the original long URL.

**Types of redirect**
There are two main types of HTTP redirects that we could use for this purpose (301/302):
- `301 (Permanent Redirect)`: This indicates that the resource has been permanently moved to the target URL. Browsers **typically cache** this response, meaning subsequent requests for the same short URL might go directly to the long URL, bypassing our server.

The response back to the client looks like this:
```
HTTP/1.1 301 Moved Permanently
Location: https://www.original-long-url.com
```
- `302 (Temporary Redirect)`: This suggests that the resource is temporarily located at a different URL. Browsers **do not cache** this response, ensuring that future requests for the short URL will always go through our server first.

The response back to the client looks like this:
```
HTTP/1.1 302 Found
Location: https://www.original-long-url.com
```
In either case, the user's browser (the client) will automatically follow the redirect to the original long URL and users will never even know that a redirect happened.
For a URL shortener, a 302 redirect is often preferred because:
- It gives us more control over the redirection process, allowing us to update or expire links as needed. (similar to how a symlink is a pointer to the actual file which grants more flexibility in case the underlying link is changed)
- It prevents browsers from caching the redirect, which could cause issues if we need to change or delete the short URL in the future.



**Overkill solution**
The different solutions to shortening a URL are the following:

    Random ID Generator
    Hashing Function
    Token Range

Random ID Generator solution

The Key Generation Service (KGS) queries the random identifier (ID) generation service to shorten a URL. The service generates random IDs using a random function or Universally Unique Identifiers (UUID). Multiple instances of the random ID generation service must be provisioned to meet the demand for scalability.
URL shortener; Random ID Generator Figure 24: URL shortener; Random ID Generator

The random ID generation service must be stateless to easily replicate the service for scaling. The ingress is distributed to a random ID generation service using a load balancer. The potential load-balancing algorithms to route the traffic are the following:

    round-robin
    least connection
    least bandwidth
    modulo-hash function
    consistent hashing

The consistent hashing or the modulo-hash function-based load balancing algorithms might result in unbalanced (hot) replicas when the same long URL is entered by a large number of clients at the same time. The KGS must verify if the generated short URL already exists in the database because of the randomness in the output.

The random ID generation solution has the following tradeoffs:

    the probability of collisions is high due to randomness
    breaks the 1-to-1 mapping between a short URL and a long URL
    coordination between servers is required to prevent a collision
    frequent verification of the existence of a short URL in the database is a bottleneck

An alternative to the random ID generation solution is using Twitter’s Snowflake8. The length of the snowflake output is 64 bits. The base62 encoding of snowflake output yields an 11-character output because each base62 encoded character consumes 6 bits. The snowflake ID is generated by a combination of the following entities (real-world implementation might vary):

    Timestamp
    Data center ID
    Worker node ID
    Sequence number

Twitter Snowflake ID Figure 25: Twitter Snowflake ID

The downsides of using snowflake ID for URL shortening are the following:

    probability of collision is higher due to the overlapping bits
    generated short URL becomes predictable due to known bits
    increases the complexity of the system due to time synchronization between servers

In summary, do not use the random ID generator solution for shortening a URL.
Hashing Function solution

The KGS queries the hashing function service to shorten a URL. The hashing function service accepts a long URL as an input and executes a hash function such as the message-digest algorithm (MD5) to generate a short URL9. The length of the MD5 hash function output is 128 bits. The hashing function service is replicated to meet the scalability demand of the system.
URL shortener; Hashing the long URL Figure 26: URL shortener; Hashing the long URL

The hashing function service must be stateless to easily replicate the service for scaling. The ingress is distributed to the hashing function service using a load balancer. The potential load-balancing algorithms to route the traffic are the following:

    weighted round-robin
    least response time
    IP address hash
    modulo-hash function
    consistent hashing

The hash-based load balancing algorithms result in hot replicas when the same long URL is entered by a large number of clients at the same time. The non-hash-based load-balancing algorithms result in redundant operations because the MD5 hashing function produces the same output (short URL) for the same input (long URL).
URL shortener; Hashing function service Figure 27: URL shortener; Hashing function service

The base62 encoding of MD5 output yields 22 characters because each base62 encoded character consumes 6 bits and MD5 output is 128 bits. The encoded output must be truncated by considering only the first 7 characters (42 bits) to keep the short URL readable. However, the encoded output of multiple long URLs might yield the same prefix (first 7 characters), resulting in a collision. Random bits are appended to the suffix of the encoded output to make it nonpredictable at the expense of short URL readability.
URL shortener; Truncating the encoded MD5 output Figure 28: URL shortener; Truncating the encoded MD5 output

An alternative hashing function for URL shortening is SHA256. However, the probability of a collision is higher due to an output length of 256 bits. The tradeoffs of the hashing function solution are the following:

    predictable output due to the hash function
    higher probability of a collision

In summary, do not use the hashing function solution for shortening a URL.
Token Range solution

The KGS queries the token service to shorten a URL. An internal counter function of the token service generates the short URL and the output is monotonically increasing.
URL shortener; Token service in consistent hash ring Figure 29: URL shortener; Token service in consistent hash ring

The token service must be horizontally partitioned (shard) to meet the scalability requirements of the system. The potential sharding schemes for the token service are the following:

    list partitioning
    modulus partitioning
    consistent hashing

The list and modulus partitioning schemes do not meet the scalability requirements of the system because both schemes limit the number of token service instances. The sharding based on consistent hashing fits the system requirements as the token service scales out by provisioning new instances.

The ingress is distributed to the token service using a load balancer. The percent-encoded long URLs are load-balanced using consistent hashing to preserve the 1-to-1 mapping between the long and short URLs. However, a load balancer based on consistent hashing might result in hot shards when the same long URL is entered by a large number of clients at the same time.

The output of the token service instances must be non-overlapping to prevent a collision. A highly reliable distributed service such as Apache Zookeeper or Amazon DynamoDB is used to coordinate the output range of token service instances. The service that coordinates the output range between token service instances is named the token range service.
URL shortener; Token range service Figure 30: URL shortener; Token range service

When the key-value store is chosen as the token range service, the quorum must be set to a higher value to increase the consistency of the token range service. The stronger consistency prevents a range collision by preventing fetching the same output range by multiple token services.

When an instance of the token service is provisioned, the fresh instance executes a request for an output range from the token range service. When the fetched output range is fully exhausted, the token service requests a fresh output range from the token range service.
URL shortener; Token range service Figure 31: URL shortener; Token range service

The token range service might become a bottleneck if queried frequently. Either the output range or the number of token range service replicas must be incremented to improve the reliability of the system. The token range solution is collision-free and scalable. However, the short URL is predictable due to the monotonically increasing output range. The following actions degrade the predictability of the shortened URL:

    append random bits to the suffix of the output
    token range service gives a randomized output range

The time complexity of short URL generation using token service is constant O(1). In contrast, the KGS must perform one of the following operations before shortening a URL to preserve the 1-to-1 mapping:

    query the database to check the existence of the long URL
    use the putIfAbsent procedure to check the existence of the long URL

Querying the database is an expensive operation because of the disk input/output (I/O) and most of the NoSQL data stores do not support the putIfAbsent procedure due to eventual consistency.
URL shortener; Bloom filter Figure 32: URL shortener; Bloom filter

A bloom filter is used to prevent expensive data store lookups on URL shortening. The time complexity of a bloom filter query is constant O(1)10. The KGS populates the bloom filter with the long URL after shortening the long URL. When the client enters a customized short URL, the KGS queries the bloom filter to check if the long URL exists before persisting the custom short URL into the data store. However, the bloom filter query might yield false positives, resulting in a database lookup. In addition, the bloom filter increases the operational complexity of the system.

When the client enters an already existing long URL, the KGS must return the appropriate short URL but the database is partitioned with the short URL as the partition key. The short URL as the partition key resonates with the read and write paths of the URL shortener.
URL shortener; Inverted index data store (Long URL: Short URL) Figure 33: URL shortener; Inverted index data store (Long URL: Short URL)

A naive solution to finding the short URL is to build an index on the long URL column of the data store. However, the introduction of a database index degrades the write performance and querying remains complex due to sharding using the short URL key.

The optimal solution is to introduce an additional data store (inverted index) with mapping from the long URLs to the short URLs (key-value schema). The additional data store improves the time complexity of finding the short URL of an already existing long URL record. On the other hand, an additional data store increases storage costs. The additional data store is partitioned using consistent hashing. The partition key is the long URL to quickly find the URL record. A key-value store such as DynamoDB is used as the additional data store.
URL shortener; Scaling the token service Figure 34: URL shortener; Scaling the token service

The token service stores some short URLs (keys) in memory so that the token service quickly provides the keys to an incoming request. The keys in the token service must be distributed by an atomic data structure to handle concurrent requests. The output range stored in token service memory is marked as used to prevent a collision. The downside of storing keys in memory is losing the specific output range of keys on a server failure. The output range must be moved out to an external cache server to scale out the token service and improve its reliability.
URL shortener; Token server Figure 35: URL shortener; Token server

The output of the token service must be encoded within the token server using an encoding service to prevent external network communication. An additional function executes the encoding of token service output.

In summary, use the token range solution for shortening a URL.
Read path

The server redirects the shortened URL to the original long URL. The simplified block diagram of a single-machine URL redirection is the following:
Simplified URL redirection Figure 36: Simplified URL redirection

The single-machine solution does not meet the scalability requirements of URL redirection for a read-heavy system. The disk I/O due to frequent database access is a potential bottleneck.

The URL redirection traffic (Egress) is cached following the 80/20 rule to improve latency. The cache stores the mapping between the short URLs and the long URLs. The cache handles uneven traffic and traffic spikes in URL redirection. The server must query the cache before hitting the data store. The cache-aside pattern is used to update the cache. When a cache miss occurs, the server queries the data store and populates the cache. The tradeoff of using the cache-aside pattern is the delay in initial requests. As the data stored in the cache is memory bound, the Least Recently Used (LRU) policy is used to evict the cache when the cache server is full.
URL redirection; Caching at different layers Figure 37: URL redirection; Caching at different layers

The cache is introduced at the following layers of the system for scalability:

    client
    content delivery network (CDN)
    reverse proxy
    dedicated cache servers

A shared cache such as CDN or a dedicated cache server reduces the load on the system. On the other hand, the private cache is only accessible by the client and does not significantly improve the system’s performance. On top of that, the definition of TTL for the private cache is crucial because private cache invalidation is difficult. Dedicated cache servers such as Redis or Memcached are provisioned between the following system components to further improve latency:

    server and data store
    load balancer and server

The typical usage pattern of a URL shortener by the client is to shorten a URL and access the short URL only once. The cache update on a single access usage pattern results in cache thrashing. A bloom filter on short URLs is introduced on cache servers and CDN to prevent cache thrashing. The bloom filter is updated on the initial access to a short URL. The cache servers are updated only when the bloom filter is already set (multiple requests to the same short URL).
URL redirection; Cache update Figure 38: URL redirection; Cache update

The cache and the data store must not be queried if the short URL does not exist. A bloom filter on the short URL is introduced to prevent unnecessary queries. If the short URL is absent in the bloom filter, return an HTTP status code of 404. If the short URL is set in the bloom filter, delegate the redirection request to the cache server or the data store.

The cache servers are scaled out by performing the following operations:

    partition the cache servers (use the short URL as the partition key)
    replicate the cache servers to handle heavy loads using leader-follower topology
    redirect the write operations to the leader
    redirect all the read operations to the follower replicas

URL redirection; Scaling cache servers Figure 39: URL redirection; Scaling cache servers

When multiple identical requests arrive at the cache server at the same time, the cache server will collapse the requests and will forward a single request to the origin server on behalf of the clients. The response is reused among all the clients to save bandwidth and system resources.
URL redirection; Cache server collapsed forwarding Figure 40: URL redirection; Cache server collapsed forwarding

The following intermediate components are introduced to satisfy the scalability demand for URL redirection:

    Domain Name System (DNS)
    Load balancer
    Reverse proxy
    CDN
    Controller service to automatically scale the services

URL redirection workflow Figure 41: URL redirection workflow

The following smart DNS services improve URL redirection:

    weighted round-robin
    latency based
    geolocation based

The reverse proxy is used as an API Gateway. The reverse proxy executes SSL termination and compression at the expense of increased system complexity. When an extremely popular short URL is accessed by thousands of clients at the same time, the reverse proxy collapse forwards the requests to reduce the system load. The load balancer must be introduced between the following system components to route traffic between the replicas or shards:

    client and server
    server and database
    server and cache server

The CDN serves the content from locations closer to the client at the expense of increased financial costs. The Pull CDN approach fits the URL redirection requirements. A dedicated controller service is provisioned to automatically scale out or scale down the system components based on the system load.

The microservices architecture improves the fault tolerance of the system. The services such as Etcd or Zookeeper help services find each other (known as service discovery). In addition, the Zookeeper is configured to monitor the health of the services in the system by sending regular heartbeat signals. The downside of microservices architecture is the increased operational complexity.
