## 1BRC Challenge

### Preparing measurements
```/bin/sh

# switch to java21
java21

# mvn clean
./mvnw clean verify

# generate 1B rows file
./create_measurements.sh 1000000000


```

### Running locally
```/bin/sh
# generate baseline for running on local
time 1brc/calculate_average_baseline.sh >outputs/baseline.log

# build go bin and run attempts
# this will time and assert results against baseline file
make run > outputs/test.log 2>outputs/test.log
```

### Baseline
```/bin/sh
time 1brc/calculate_average_baseline.sh >outputs/baseline.log

201.71s user 10.06s system 94% cpu 3:43.09 total --> 3 minutes 21.71 seconds
```

### Attempt 1
- Use buffered reader single threaded, no parallelization.
- Use int for storing temp instead of float.

```/bin/sh
2025/01/28 15:42:18 INFO running benchmark bm.name=a1
2025/01/28 15:42:18 INFO a1 start=2025-01-28T15:42:18.915+08:00
2025/01/28 15:44:17 INFO done aggregating results
2025/01/28 15:44:17 INFO a1 time_elapsed=1m58.906493417s time_start=2025-01-28T15:42:18.915+08:00 time_end=2025-01-28T15:44:17.819+08:00
```

### Attempt 2
- Use multiple goroutines for concurrency. Single goroutine reads file and publishes parsed values to chan for consumers to aggregate.

```/bin/sh
no go gave up waiting
```

### Attempt 3
- Similar to attempt 2 except instead of using single goroutine to read file, split file into chunks and get goroutines to read files concurrently.
```/bin/sh
2025/01/28 15:31:02 INFO running benchmark bm.name=a3
2025/01/28 15:31:02 INFO a3 start=2025-01-28T15:31:02.053+08:00
...
2025/01/28 15:31:40 INFO a3 time_elapsed=38.472410959s time_start=2025-01-28T15:31:02.053+08:00 time_end=2025-01-28T15:31:40.524+08:00
```
