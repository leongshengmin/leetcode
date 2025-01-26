## 1BRC Challenge

### Local Testing
```/bin/sh

# switch to java21
java21

# mvn clean
./mvnw clean verify

# generate 1B rows file
./create_measurements.sh 1000000000

# generate baseline for running on local
time ./calculate_average_baseline.sh
```

### Baseline
```
./calculate_average_baseline.sh  191.44s user 6.59s system 98% cpu 3:20.91 total
```

### Attempt 1
- Use buffered reader single threaded, no parallelization.
- Use int for storing temp instead of float.
```
make run  0.17s user 0.19s system 122% cpu 0.290 total
```
