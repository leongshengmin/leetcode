package onebrc

import (
	"bufio"
	"log/slog"
	"os"
)

type Attempt1 struct{}

// single threaded / goroutine
func (a *Attempt1) Run(filename string) (map[string][NumMetrics]int, error) {
	file, err := os.Open(filename)
	if err != nil {
		slog.Error("error reading from file", "file", filename, "err", err)
		return nil, err
	}
	defer file.Close()

	// create map to store agg results
	aggTempByStation := map[string][NumMetrics]int{}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		station, temp, err := ReadBufferedFromFile(scanner)
		if err != nil {
			if err == SkippableLineErr {
				continue
			}
			slog.Error("error reading from file", "err", err)
			return nil, err
		}

		// update agg results
		UpdateAggMapWithResults(aggTempByStation, station, temp)
	}
	slog.Info("done aggregating results")

	return aggTempByStation, nil
}
