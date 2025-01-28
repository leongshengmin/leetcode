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
# TODO
```

### Attempt 2
- Use multiple goroutines for parallelization. Map reduce pattern.

```/bin/sh
# TODO
```
