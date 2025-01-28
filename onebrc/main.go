package main

import (
	"log/slog"
	"main/onebrc"
	"time"
)

/**
* Write a program for retrieving temperature measurement values from a text file
* and calculating the min, mean, and max temperature per weather station.
* file has 1,000,000,000 rows!
*
* sample of the file:
* Hamburg;12.0
* Bulawayo;8.9
* Palembang;38.8
* St. John's;15.2
* Cracow;-12.6

*
min,avg,max
* {Abha=-23.0/18.0/59.2, Abidjan=-16.2/26.0/67.3, Abéché=-10.0/29.4/69.0, ...}
**/

type OneBRCRunner interface {
	Run(filename string) (map[string][onebrc.NumMetrics]int, error)
}

// max, min, sum, count
const filePath = "/Users/leongshengmin/Documents/leetcode/onebrc/1brc/measurements.txt"

func main() {
	// a1 := &onebrc.Attempt1{}
	a2 := &onebrc.Attempt2{}
	benchmarks := []struct {
		name   string
		runner OneBRCRunner
	}{
		// {"a1", a1},
		{"a2", a2},
	}

	// run benchmarks
	for _, bm := range benchmarks {
		aggTempByStation, err := timeFuncCallElapsed(bm.name, bm.runner, filePath)
		if err != nil {
			slog.Error("failed to run benchmark", "bm.name", bm.name, "err", err)
			return
		}
		onebrc.OutputResultToStdOut(aggTempByStation, true)
	}
}

func timeFuncCallElapsed(name string, runner OneBRCRunner, filename string) (map[string][onebrc.NumMetrics]int, error) {
	time_now := time.Now()
	res, err := runner.Run(filename)
	time_elapsed := time.Since(time_now)
	slog.Info(name, "time_elapsed", time_elapsed)
	return res, err
}
