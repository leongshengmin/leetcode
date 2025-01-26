package onebrc

import (
	"bufio"
	"fmt"
	"io"
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
)

// readStringUntilDelimiter reads a string from the provided bufio.Reader, excluding the specified end delimiter byte.
// This function is necessary because the standard bufio.ReadString implementation includes the delimiter in the returned string.
// The function skips over any leading delimiter bytes and returns the string up to but not including the first occurrence of the end delimiter.
// If the end of the reader is reached before the delimiter is found, the function returns the string read so far and an io.EOF error.
func readStringUntilDelimiter(reader *bufio.Reader, endDelimiter byte) (string, error) {
	// reads string using bufio reader excluding delimiter
	// unable to use bufio readString impl as that includes delimiter
	sb := strings.Builder{}
	for {
		byteArr, err := reader.Peek(1)
		if err != nil {
			if err == io.EOF {
				return sb.String(), err
			}
			slog.Error("error reading byte using peek op", "err", err)
			break
		}
		// if next char is end delimiter
		// we should return the bytes in buffer
		if byteArr[0] == endDelimiter {
			return sb.String(), nil
		}
		b, err := reader.ReadByte()
		if err != nil {
			slog.Error("error reading byte", "err", err)
			return sb.String(), io.EOF
		}
		// skip and exclude delimiters from result
		// these delimiters may occur at start of the string
		if b == semiColonDelim || b == periodDelim || b == newLineDelim {
			continue
		}
		sb.WriteByte(b)
	}
	return sb.String(), nil
}

// outputResultToStdOut aggregates temperature metrics by station and prints the results to standard output.
// The output is formatted as a JSON-like object, with each station's metrics displayed as a key-value pair.
// The metrics displayed for each station are the minimum, average, and maximum temperature values.
func OutputResultToStdOut(aggTempByStation map[string][NumMetrics]int) {
	// create slice of stations to sort output by
	stations := make([]string, 0, len(aggTempByStation))
	for station := range aggTempByStation {
		stations = append(stations, station)
	}
	sort.Strings(stations)

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

// ReadBufferedFromFile reads a station identifier and temperature value from a buffered reader.
// It returns the station name, the temperature value, and any error that occurred during reading.
// The temperature value is stored as an integer, with the decimal portion scaled by tempScalingFactor.
func ReadBufferedFromFile(reader *bufio.Reader) (string, int, error) {
	// read buffered from file
	station, err := readStringUntilDelimiter(reader, semiColonDelim)
	if err != nil {
		if err == io.EOF {
			return "", -1, io.EOF
		}
		slog.Error("error reading station", "err", err)
		return "", -1, err
	}
	tempIntStr, _ := readStringUntilDelimiter(reader, periodDelim)
	tempDecStr, _ := readStringUntilDelimiter(reader, newLineDelim)
	tempInt, err := strconv.Atoi(tempIntStr)
	tempDec, err := strconv.Atoi(tempDecStr)
	if err != nil {
		return "", -1, io.EOF
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
