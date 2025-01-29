package onebrc

import (
	"bufio"
	"fmt"
	"log/slog"
	"os"
	"sort"
	"strconv"
	"strings"
)

const (
	// external constants
	// number of metrics to track -- max, min, sum, count
	NumMetrics = 4

	// index of each metric in the aggTempByStation map
	max_value_index   = 0
	min_value_index   = 1
	sum_value_index   = 2
	count_value_index = 3

	// scaling factor for temperature values
	tempScalingFactor = 10

	// delimiters
	semiColonDelim = ';'
	periodDelim    = '.'
	newLineDelim   = '\n'

	// expected number of stations
	// awk -F';' '{print $1}' 1brc/data/weather_stations.csv | sort | uniq | wc -l
	// 41345
	expectedNumStations = 413
)

// numConsumerGoroutines is the number of consumer goroutines to start
var numConsumerGoroutines = 16

// outputResultToStdOut aggregates temperature metrics by station and prints the results to standard output.
// The output is formatted as a JSON-like object, with each station's metrics displayed as a key-value pair.
// The metrics displayed for each station are the minimum, average, and maximum temperature values.
func OutputResultToStdOut(aggTempByStation map[string][NumMetrics]int, enableAssertion bool) {
	// create slice of stations to sort output by
	stations := make([]string, 0, len(aggTempByStation))
	for station := range aggTempByStation {
		stations = append(stations, station)
	}
	sort.Strings(stations)

	// assert results
	if enableAssertion {
		assertResults(len(stations), expectedNumStations)
	}

	// aggregate results
	// and print to stdout
	fmt.Fprint(os.Stdout, "{")
	for i, station := range stations {
		if i > 0 {
			fmt.Fprint(os.Stdout, ", ")
		}
		metricVals := aggTempByStation[station]
		// convert to float32 as original values are stored as ints
		maxVF, minVF, avgVF := float32(metricVals[0])/tempScalingFactor, float32(metricVals[1])/tempScalingFactor, float32(metricVals[2])/float32(metricVals[3])
		fmt.Fprintf(os.Stdout, "%s=%.1f/%.1f/%.1f", station, minVF, avgVF, maxVF)
	}
	fmt.Fprint(os.Stdout, "}\n")
}

// assertResults checks that the number of stations in the provided slice matches the expected number.
// If the number of stations does not match, it logs an error and panics with an error message.
func assertResults(actualNumStations int, expectedNumStations int) {
	// assert that we have the expected number of stations
	if actualNumStations != expectedNumStations {
		slog.Error("unexpected number of stations", "expected", expectedNumStations, "actual", actualNumStations)
		panic(fmt.Errorf("expected number of stations to be %d, got %d", expectedNumStations, actualNumStations))
	}
}

var SkippableLineErr error

// improved version compared to ReadBufferedFromFile
func ReadBufferedFromFile(scanner *bufio.Scanner) (string, int, error) {
	// read buffered from file
	line := scanner.Text()
	station, tempStr, hasSemi := strings.Cut(line, ";")
	if !hasSemi {
		return "", -1, SkippableLineErr
	}
	tempIntStr, tempDecStr, hasPeriod := strings.Cut(tempStr, ".")
	if !hasPeriod {
		return "", -1, SkippableLineErr
	}
	tempInt, err := strconv.Atoi(tempIntStr)
	tempDec, err := strconv.Atoi(tempDecStr)
	if err != nil {
		return "", -1, err
	}

	// store temp as int not float
	temp := -1
	if tempInt < 0 {
		temp = tempInt*tempScalingFactor - tempDec
	} else {
		temp = tempInt*tempScalingFactor + tempDec
	}
	return station, temp, nil

}

// UpdateAggMapWithResults updates the aggregation map aggTempByStation with the temperature reading for the given station.
// If the station is not yet in the map, it initializes the metrics for that station.
// Otherwise, it updates the min, max, sum, and count metrics for the station.
func UpdateAggMapWithResults(aggTempByStation map[string][NumMetrics]int, station string, temp int) {
	metricVals, ok := aggTempByStation[station]
	if !ok {
		aggTempByStation[station] = [NumMetrics]int{temp, temp, temp, 1}
	} else {
		maxV, minV, sumV, countV := metricVals[max_value_index], metricVals[min_value_index], metricVals[sum_value_index], metricVals[count_value_index]
		aggTempByStation[station] = [NumMetrics]int{max(maxV, temp), min(minV, temp), sumV + temp, countV + 1}
	}
}
