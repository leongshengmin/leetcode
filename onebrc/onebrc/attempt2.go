package onebrc

import (
	"bufio"
	"io"
	"log/slog"
	"os"
	"sync"
)

type Attempt2 struct{}
type DataPoint struct {
	Station string
	Temp int
}

// TODO fix this implementation -- not working
// numConsumerGoroutines is the number of consumer goroutines to start
const numConsumerGoroutines = 4

func (a *Attempt2) Run(filename string) (map[string][NumMetrics]int, error) {
	file, err := os.Open(filename)
	if err != nil {
		slog.Error("error reading from file", "file", filename, "err", err)
		return nil, err
	}
	defer file.Close()

	inputs := make(chan *DataPoint)
	resultsChan := make(chan map[string][NumMetrics]int)
	var wg sync.WaitGroup

	// close results chan
	defer close(resultsChan)

	reader := bufio.NewReader(file)

	// start consumer goroutines to get agg values
	for range numConsumerGoroutines {
		// increment wg for each goroutine
		wg.Add(1)
		go startWorker(inputs, resultsChan)
	}

	go func() {
		for {
			// read buffered from file
			station, temp, err := ReadBufferedFromFile(reader)
			if err != nil {
				if err == io.EOF {
					break
				}
				slog.Error("error reading from file", "err", err)
				return // exit goroutine
			}
			inputs <- &DataPoint{
				Station: station,
				Temp: temp,
			}
		}
		defer close(inputs)
	}()

	// merge results
	aggResult := map[string][NumMetrics]int{}
	for res := range resultsChan {
		for station, metricVals := range res {
			maxV, minV, sumV, countV := metricVals[max_value_index], metricVals[min_value_index], metricVals[sum_value_index], metricVals[count_value_index]
			aggV, ok := aggResult[station]
			if !ok {
				aggResult[station] = [4]int{maxV, minV, sumV, countV}
				continue
			}
			aggResult[station] = [4]int{max(maxV, aggV[max_value_index]), min(minV, aggV[min_value_index]), sumV + aggV[sum_value_index], countV + aggV[count_value_index]}
		}
		// decrement wg each time we get 1 result from chan
		wg.Done()
	}

	// block till all goroutines done
	wg.Wait()

	return aggResult, nil
}

func startWorker(inputs <-chan *DataPoint, res chan map[string][NumMetrics]int) {
	// create map to store agg results per worker so we don't share state
	aggTempByStation := map[string][NumMetrics]int{}

	// update aggregation map with results
	for {
		select {
		case d, ok := <-inputs:
			if !ok {
				// output results to channel once no more inputs ie chan closed
				res <- aggTempByStation
				return
			}
			UpdateAggMapWithResults(aggTempByStation, d.Station, d.Temp)
		}
	}
}
