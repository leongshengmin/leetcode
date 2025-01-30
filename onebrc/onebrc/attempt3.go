package onebrc

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"log/slog"
	"os"
)

type Attempt3 struct{}

func (a *Attempt3) Run(filename string) (map[string][NumMetrics]int16, error) {
	splits, err := splitFile(filename, numConsumerGoroutines)
	if err != nil {
		slog.Error("error splitting file", "err", err)
		return nil, err
	}

	// create buffered channels allowing parallel reads from number of goroutines
	resultsChan := make(chan *map[string][NumMetrics]int16, numConsumerGoroutines)
	defer close(resultsChan)

	// start consumer goroutines to get agg values
	for i := range numConsumerGoroutines {
		split := splits[i]
		go startWorkerProcessPart(i, filename, split.offset, split.size, resultsChan)
	}

	// merge results from goroutines whenever they come in to results chan
	// this will block until all results are published
	aggResult := map[string][NumMetrics]int16{}
	for range numConsumerGoroutines {
		// block till we get something from the results chan
		res := <-resultsChan
		slog.Debug("received result from worker")
		for station, metricVals := range *res {
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

func startWorkerProcessPart(workerID int, filename string, fileOffset int64, partSize int64, res chan<- *map[string][NumMetrics]int16) {
	slog.Debug("starting worker", "workerID", workerID, "fileOffset", fileOffset)
	file, err := os.Open(filename)
	if err != nil {
		slog.Error("error reading from file", "file", filename, "err", err)
		panic(err)
	}
	defer file.Close()
	_, err = file.Seek(fileOffset, io.SeekStart)
	if err != nil {
		panic(err)
	}

	// create buffered reader
	limitedReader := io.LimitedReader{R: file, N: partSize}
	scanner := bufio.NewScanner(&limitedReader)

	// create map to store agg results per worker so we don't share state
	aggTempByStation := map[string][NumMetrics]int16{}

	for scanner.Scan() {
		station, temp, err := ReadBufferedFromFile(scanner)
		if err != nil {
			if err == SkippableLineErr {
				continue
			}
			slog.Error("error reading from file")
			return
		}
		UpdateAggMapWithResults(aggTempByStation, station, temp)
	}

	slog.Debug("worker done", "workerID", workerID)
	// output results to channel once no more inputs ie chan closed
	res <- &aggTempByStation
}

type part struct {
	offset, size int64
}

func splitFile(inputPath string, numParts int) ([]part, error) {
	const maxLineLength = 100

	f, err := os.Open(inputPath)
	if err != nil {
		return nil, err
	}
	st, err := f.Stat()
	if err != nil {
		return nil, err
	}
	size := st.Size()
	splitSize := size / int64(numParts)

	buf := make([]byte, maxLineLength)

	parts := make([]part, 0, numParts)
	offset := int64(0)
	for i := 0; i < numParts; i++ {
		if i == numParts-1 {
			if offset < size {
				parts = append(parts, part{offset, size - offset})
			}
			break
		}

		seekOffset := max(offset+splitSize-maxLineLength, 0)
		_, err := f.Seek(seekOffset, io.SeekStart)
		if err != nil {
			return nil, err
		}
		n, _ := io.ReadFull(f, buf)
		chunk := buf[:n]
		newline := bytes.LastIndexByte(chunk, '\n')
		if newline < 0 {
			return nil, fmt.Errorf("newline not found at offset %d", offset+splitSize-maxLineLength)
		}
		remaining := len(chunk) - newline - 1
		nextOffset := seekOffset + int64(len(chunk)) - int64(remaining)
		parts = append(parts, part{offset, nextOffset - offset})
		offset = nextOffset
	}
	return parts, nil
}
