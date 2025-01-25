## CAP Theroem

## WAL (Translog)
WAL files are used to store the operations before writes are actually performed on data. This log exists primarily for crash-safety purposes: if the system crashes, the database can be restored to consistency by “replaying” the log entries made since the last checkpoint. However, the existence of the log makes it possible to use a third strategy for backing up databases: we can combine a file-system-level backup with backup of the WAL files. If recovery is needed, we restore the file system backup and then replay from the backed-up WAL files to bring the system to a current state.

AL's central concept is that changes to data files (where tables and indexes reside) must be written only after those changes have been logged, that is, after WAL records describing the changes have been flushed to permanent storage. If we follow this procedure, we do not need to flush data pages to disk on every transaction commit, because we know that in the event of a crash we will be able to recover the database using the log:

Using WAL results in a significantly reduced number of disk writes, because only the WAL file needs to be flushed to disk to guarantee that a transaction is committed, rather than every data file changed by the transaction. The WAL file is written sequentially, and so the cost of syncing the WAL is much less than the cost of flushing the data pages. This is especially true for servers handling many small transactions touching different parts of the data store. Furthermore, when the server is processing many small concurrent transactions, one fsync of the WAL file may suffice to commit many transactions.

Because WAL restores database file contents after a crash, journaled file systems are not necessary for reliable storage of the data files or WAL files. In fact, journaling overhead can reduce performance, especially if journaling causes file system data to be flushed to disk. Fortunately, data flushing during journaling can often be disabled with a file system mount option, e.g., data=writeback on a Linux ext3 file system. Journaled file systems do improve boot speed after a crash.

**Elasticsearch**

in Elasticsearch, WAL is used during index recovery to replay operations that have not been performed on the segment. (For performance, can choose to async fsync translog to disk with risk of some data loss).

ext4 fs recommended, fs journaling enabled `data=writeback,relatime,nobarrier` to only journal metadata updates (not data since translog already has data).
```
data=writeback: This option specifies the journaling mode for ext3/ext4 filesystems. In writeback mode, metadata updates are journaled, but data blocks are not. This can improve performance but may risk data integrity in case of a crash.

relatime: This option is used to update the inode access times (atime) only if the previous atime is older than the modification time (mtime) or the change time (ctime). It helps reduce disk I/O by avoiding unnecessary updates.

nobarrier: This option disables the use of write barriers in journaling filesystems. Write barriers ensure that filesystem metadata is written in a specific order to preserve data integrity, particularly in case of power failure. Disabling it (nobarrier) can improve performance but may risk data corruption in certain situations.
```

**Postgresql**
in Postgresql, WAL files store all operations performed on tables, data and can be used to restore the WHOLE database (compared to ES wherein translog is only used to replay part of the operations onto a segment from the primary shard instead of the whole DB). Each translog operation is buffered in the WAF buffer before being fsynced to disk (similar to ES). Once the WAL file gets large enough, WAL files can be archived to remote store before being removed from disk.

## Change-Data-Capture
![cdc_methods](cdc_methods.png)
1. Batch - Queries
Running periodic SQL queries to capture changes occuring within a certain time window.
e.g. sql query
```
SELECT * FROM my_table WHERE time_updated > time_last_query’;
```
Advantages of Queries-Based Postgres CDC:
- Simple to set up: Requires no special configuration beyond writing SQL queries.
- Low resource usage: Has minimal impact on the source system since it only pulls data at scheduled intervals.

Disadvantages of Queries-Based Postgres CDC:
- High latency: Changes are not captured in real-time, leading to potential delays in data synchronization.
- Cannot capture deletions: Queries often cannot detect DELETE operations unless explicitly handled.
- Performance impact: Large queries on high-volume tables can slow down the source database if not properly managed.

2. Real-time - Triggers
Triggers are functions that automatically execute in response to insert, update, or delete operations on the source database. These changes are captured and written to a secondary table (or changelog table), which serves as a log of modifications.

How Trigger-Based Postgres CDC works:
- You define triggers that listen for changes to a table (inserts, updates, deletes).
- When changes occur, the triggers fire and write the changes to a dedicated table.
- The captured changes can then be extracted and moved to the target system.
e.g. sql query to capture changes in changelog table
```
SELECT audit.audit_table('changelog_table_name');
```

Advantages of Trigger-Based Postgres CDC:
- Capture all change types: Triggers can detect INSERT, UPDATE, and DELETE operations, ensuring comprehensive tracking of changes.
- Real-time data capture: Changes are immediately recorded when they happen, offering low-latency synchronization.

Disadvantages of Trigger-Based Postgres CDC:
- Performance impact: Triggers can slow down database operations, especially on high-traffic tables, as each data modification needs to trigger an action.
- Complex setup: Setting up triggers requires careful planning, especially when dealing with large tables or complex business logic.
- Changelog management: The log of changes can grow quickly, necessitating cleanup and management to avoid performance issues.

3. Real-time, less performance impact - WAL
WAL records every change made to the database and is used for recovery and data integrity purposes. By leveraging logical replication and decoding features, you can stream these WAL changes to external systems in near real-time.

How WAL for Postgres CDC works:
- Logical replication enables you to capture changes from the WAL.
- Logical decoding converts the WAL entries into a consumable format (like JSON or SQL).
- The changes are then streamed to a target system using tools like Kafka, RabbitMQ, or custom connectors.

Advantages of Using WAL for Postgres CDC:
- Real-time data synchronization: Changes are captured and propagated to target systems almost immediately.
- Minimal impact on database performance: The use of WAL allows for efficient data capture with minimal overhead on the source database.
- Scalability: Ideal for large-scale systems with high-volume transactional data.

Disadvantages of Using WAL for Postgres CDC:
- Complex setup: Requires setting up logical replication, decoding, and potentially integrating third-party tools like Kafka, Debezium, or Estuary Flow. Estuary Flow offers an intuitive alternative for managing CDC pipelines with easy integration into PostgreSQL systems.
- Requires advanced PostgreSQL knowledge: Configuring WAL for CDC requires familiarity with PostgreSQL internals, which can be a steep learning curve for beginners.

Implementation
1. Set `wal_level` to logical to allow the DB to record logical changes req'd for replication.
```
ALTER SYSTEM SET wal_level = logical;
```
2. Ensure DB user has replication/read privileges for performing logical replication.
```
ALTER ROLE your_user_name WITH REPLICATION; -- allow user replication priv
GRANT pg_read_all_data TO your_user_name; -- grant read access to all tabs for logical replication
```
3. Ensure source tabs have a primary key; alternatively set REPLICA IDENTITY FULL (with performance implications).
Logical replication requires source tables have a pk to identify rows uniquely. If a table does not have a pk, you can set its replication identify to full with performance implications. 
> A published table must have a replica identity configured in order to be able to replicate UPDATE and DELETE operations, so that appropriate rows to update or delete can be identified on the subscriber side. By default, this is the primary key, if there is one. Another unique index (with certain additional requirements) can also be set to be the replica identity. If the table does not have any suitable key, then it can be set to replica identity FULL, which means the entire row becomes the key.
4. Create a publication for the source tables to let postgresql know what DML operations e.g. `insert/update/delete/update` should be published.
```
CREATE PUBLICATION my_publication FOR TABLE my_table WITH publish 'insert, update, delete';
```
4. Perform logical decoding to convert WAL to another format e.g. JSON / SQL / Protobuf. For this you might need to install a plugin e.g. `wal2json` / `pgoutput`.
5. Setup Kafka topic to store the published decoded event logs for downstream consumers to consume.
