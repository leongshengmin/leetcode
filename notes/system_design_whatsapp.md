features:
- messaging (minimally 1:1)
- last seen activity
- sending images / media
- encryption
- supports calls

client A (send message to client B) -> gateway -> user service (for checking if B exists and A can connect to B) -> kafka (for storing message event) -> message service (subscribes to message sent event and routes message event to B + persists message in messages table) -> activity service (check if B is online + if so the process holding websocket conn to B) -> message service (sends message to B via gateway over websocket connection to B after getting process holding websocket conn to B) -> gateway -> client B

if B is offline
-> message service (publish message to kafka for eventnotifications service to do cloud notif) -> kafka -> eventnotifications service

client -> api gateway -> kafka (for storing events e.g. read receipts) -> events service (sends events back to same gateway that client is connecting to)
use websockets for bidirectional connections st server can send read receipts to client
can use long polling ie client polls server for batch of messages but not real time
 
client (sends ping liveness check to show its still online) -> api gateway -> kafka (last seen time) -> activity service -> update last seen in DB


cache access patterns:
- write through (write to cache then to DB then return success)
- write around (write directly to DB; read causes cache miss that reads from DB)
- write back (write to cache then return to client success; write to DB happens async)


consistency in distributed systems
- use tcp since ordered and acks

2 phase commit (prepare -> commit)
For transaction ID x
- leader publishes change request to N followers
- leader waits for at least (N/2) followers to ACK;
    - if publish fails, leader can retry the txn (since we use transactions, we ensure idenpotency). But once we exhaust retries, we have to fail and rollback txn.
    - if leader doesn't get sufficient responses then leader rolls back and publishes rollback message to followers. (Here followers are braindead and rely on leader to think)
- leader commits req and publishes commit req to followers to also commit
transaction ends

Note that if we want perfect consistency, we need to take row locks on all replicas of the row before the entire transaction goes through on leaders + followers.
- performance cost since we need all copies of data to be persisted
- we give up availability since if we have < N copies of data available, reads + writes will fail

Therefore most systems have eventual consistency wherein you choose how many acks you require from the copies of data. (e.g. for kafka you can give up on consistency which is the default behaviour by reducing the acks)

Kafka is consistent + available / partition tolerant:
>Each shard has a single leader. The leader maintains a set of in-sync-replicas: all the nodes which are up-to-date with the leader’s log, and actively acknowledging new writes. Every write goes through the leader and is propagated to every node in the In Sync Replica set, or ISR. Once all nodes in the ISR have acknowledged the request, the leader considers it committed, and can ack to the client.
This is of note because most CP systems only claim tolerance to n/2-1 failures; e.g. a majority of nodes must be connected and healthy in order to continue. 

Kafka attains this CP goal by allowing the ISR to shrink to just one node: the leader itself. In this state, the leader is acknowledging writes which have been only been persisted locally. What happens if the leader then loses its Zookeeper claim?

The system cannot safely continue–but the show must go on. In this case, Kafka holds a new election and promotes any remaining node–which could be arbitrarily far behind the original leader. That node begins accepting requests and replicating them to the new ISR.

When the original leader comes back online, we have a conflict. The old leader is identical with the new up until some point, after which they diverge. 

If a topic is configured with only two replicas and one fails (i.e., only one in sync replica remains), then writes that specify acks=all will succeed. However, these writes could be lost if the remaining replica also fails. Although this ensures maximum availability of the partition, this behavior may be undesirable to some users who prefer durability over availability. Therefore, we provide two topic-level configurations that can be used to prefer message durability over availability:

    CP : Disable unclean leader election - if all replicas become unavailable, then the partition will remain unavailable until the most recent leader becomes available again. This effectively prefers unavailability over the risk of message loss. See the previous section on Unclean Leader Election for clarification.

    CP: Specify a minimum ISR size - the partition will only accept writes if the size of the ISR is above a certain minimum, in order to prevent the loss of messages that were written to just a single replica, which subsequently becomes unavailable. This setting only takes effect if the producer uses acks=all and guarantees that the message will be acknowledged by at least this many in-sync replicas. This setting offers a trade-off between consistency and availability. A higher setting for minimum ISR size guarantees better consistency since the message is guaranteed to be written to more replicas which reduces the probability that it will be lost. However, it reduces availability since the partition will be unavailable for writes if the number of in-sync replicas drops below the minimum threshold.

- C: kafka requires all ISR copies to ack for write to go through. Reads happen only on isrs (ie replicas that have caught up with the most recent insync state as the leader)
- A: (if we don't set min isrs) we can lose all copies except leader. Since if replicas fail, they are taken out of isr list so number of required acks to go through decreases / increases based on number of running replicas.
- P: (if we dont set min isrs) if we lose quorum of isrs we could get 

ES is consistent + partition tolerant but not available:
- C: ES (in default settings) requires N primary + replicas to ACK before returning success for write operations. Write is replicated on primary + replica shards ie persisted to translog + indexing process repeated on each shard copy. Hence consistent since reads after write should return the same data (if we ignore segment creation / rollover). Even in segment replication, uses a similar ISR model to kafka. Hence consistent.
- A: not available since if primary + replica shards unavailable then writes will fail.
- P: we can lose all shards except primary shard


CAP:
- if you want consistency, you need locks (sql) -- CA (mysql, postgresql)
- nosql (for aggregations, scale, eventual consistency most of the time) (CP / AP)
    - CP: mongodb, redis (single server), elasticsearch
    - AP: clickhouse, cassandra, redis (clustered)
    > MongoDB is a popular NoSQL database management system that is used for big data applications running across multiple locations. MongoDB resolves network partitions by maintaining consistency, sacrificing availability as necessary in the event of failure. One primary node receives all write operations in MongoDB. The system needs to elect a new primary node if the existing one becomes unavailable, and while it does, clients can’t make any write requests so data remains consistent.
    > In contrast to MongoDB, Apache Cassandra is an open source NoSQL database with a peer-to-peer architecture and potentially multiple points of failure. CAP theorem in Cassandra reveals an AP database: Cassandra offers availability and partition tolerance but can’t provide consistency all the time. However, by reconciling inconsistencies as quickly as possible and allowing clients to write to any nodes at any time, Cassandra provides eventual consistency. Inconsistencies are resolved quickly in most cases of network partitions, so the constant availability and high performance are often worth the Cassandra CAP theorem trade-off.


prepared stmts for combating sql injections
in golang instead of string interpolation use '?' which causes sql server to evaluate the sql stmt and value separately and validate ? as a value rather than sql stmt.

immutability of segments/data --> cache friendly + supports versioning
- always create new segments with some version id
- compaction to cleanup old segments

hashing and collision:
- hash(key) + linear probing to find empty slot
- hash(key) + linked list
- hash(key) + jump probing

how to implement LRU?
linked list of keys sorted by access time

cache write / read:
Concurrency
- multiwriter -> event queue -> single threaded event loop consumer to write to not use locks/deal with concurrency -> callback to notify write done

Fault tolerant
using WAL
- append write log operations to log file (WAL); rollover log file; 
    - write operation -> produce to WAL buffer -> single consumer append to log file -> archive to remote store
using data snapshot
- snapshot hashtable (cache data) periodically; store differential snapshots, upload to s3

Availability
- replication (fully synchronous / async / partial sync)
    - fully sync: consistency (since once writes to all replica servers succeed then write returns success)
    - async: eventual consistency (writes async replicated from leader to followers -- maintaining ISR list similar to kafka so that we know which follower servers can serve consistent reads)
    - partial sync: eventual consistency (writes need to succeed on N replica servers to succeed; remaining replica servers use async replication)

data corruption and merkle trees:
- merkle tree: tree of hashes (used in fs to compute checksums on hierarchy of files)
