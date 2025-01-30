package onebrc

import (
	"bufio"
	"log/slog"
	"os"
	"sync"
)

type Attempt2 struct{}
type DataPoint struct {
	Station string
	Temp    int16
}

func (a *Attempt2) Run(filename string) (map[string][NumMetrics]int16, error) {
	file, err := os.Open(filename)
	if err != nil {
		slog.Error("error reading from file", "file", filename, "err", err)
		return nil, err
	}
	defer file.Close()

	// create buffered channels allowing parallel reads from number of goroutines
	inputs := make(chan *DataPoint, numConsumerGoroutines)
	resultsChan := make(chan map[string][NumMetrics]int16, numConsumerGoroutines)

	scanner := bufio.NewScanner(file)

	var wg sync.WaitGroup

	// start consumer goroutines to get agg values
	for i := range numConsumerGoroutines {
		wg.Add(1)
		go startWorker(i, inputs, resultsChan, &wg)
	}

	go func() {
		// start producer to read from file
		for scanner.Scan() {
			// read buffered from file
			station, temp, err := ReadBufferedFromFile(scanner)
			if err != nil {
				if err == SkippableLineErr {
					continue
				}
				slog.Error("error reading from file", "err", err)
				return // exit
			}
			inputs <- &DataPoint{
				Station: station,
				Temp:    temp,
			}
		}
		// close input chan to let consumers know when no more data is coming
		close(inputs)
	}()

	// goroutine to close results chan
	go func() {
		// wait for all goroutines to finish publishing results
		wg.Wait()
		// close results chan once all results are published
		close(resultsChan)
	}()

	// merge results from goroutines whenever they come in to results chan
	// this will block until all results are published
	aggResult := map[string][NumMetrics]int16{}
	for res := range resultsChan {
		slog.Debug("received result from worker")
		for station, metricVals := range res {
			maxV, minV, sumV, countV := metricVals[max_value_index], metricVals[min_value_index], metricVals[sum_value_index], metricVals[count_value_index]
			aggV, ok := aggResult[station]
			if !ok {
				aggResult[station] = [4]int16{maxV, minV, sumV, countV}
				continue
			}
			aggResult[station] = [4]int16{max(maxV, aggV[max_value_index]), min(minV, aggV[min_value_index]), sumV + aggV[sum_value_index], countV + aggV[count_value_index]}
		}
	}

	return aggResult, nil
}

func startWorker(workerID int, inputs <-chan *DataPoint, res chan<- map[string][NumMetrics]int16, wg *sync.WaitGroup) {
	slog.Debug("starting worker", "workerID", workerID)
	// create map to store agg results per worker so we don't share state
	aggTempByStation := map[string][NumMetrics]int16{}

	defer func() {
		// decrement wait group
		wg.Done()
		slog.Debug("worker done", "workerID", workerID)

		// output results to channel once no more inputs ie chan closed
		res <- aggTempByStation
	}()

	// range over input channel to process inputs
	for input := range inputs {
		slog.Debug("got input", "station", input.Station, "temp", input.Temp, "workerID", workerID)
		UpdateAggMapWithResults(aggTempByStation, input.Station, input.Temp)
	}
}
