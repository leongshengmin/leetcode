package main

import (
	"flag"
	"fmt"
	"log/slog"
	"main/onebrc"
	"os"
	"runtime/pprof"
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
	Run(filename string) (map[string][onebrc.NumMetrics]int16, error)
}

// max, min, sum, count
const filePath = "/Users/leongshengmin/Documents/leetcode/onebrc/1brc/measurements.txt"

func main() {
	var (
		cpuProfile = flag.Bool("cpuprofile", false, "write CPU profile to file")
		revision   = flag.Int("revision", 2, "which revision to use")
	)

	a1 := &onebrc.Attempt1{}
	a2 := &onebrc.Attempt2{}
	a3 := &onebrc.Attempt3{}
	benchmarks := []struct {
		name   string
		runner OneBRCRunner
	}{
		{"a1", a1},
		{"a2", a2},
		{"a3", a3},
	}

	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(),
			"Usage: bin/onerbc [-cpuprofile] [-revision 2]\n")
		flag.PrintDefaults()
	}
	flag.Parse()

	// check if input file exists
	_, err := os.Stat(filePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}

	if *cpuProfile {
		f, err := os.Create("outputs/cpu.prof")
		if err != nil {
			fmt.Fprintf(os.Stderr, "error: %v\n", err)
			os.Exit(1)
		}
		pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}

	if *revision < 1 || *revision > len(benchmarks) {
		fmt.Fprintf(os.Stderr, "invalid revision %d\n", *revision)
		os.Exit(1)
	}

	// run benchmarks
	bm_idx := *revision - 1
	bm := benchmarks[bm_idx]
	slog.Info("running benchmark", "bm.name", bm.name)
	aggTempByStation, err := timeFuncCallElapsed(bm.name, bm.runner, filePath)
	if err != nil {
		slog.Error("failed to run benchmark", "bm.name", bm.name, "err", err)
		return
	}
	onebrc.OutputResultToStdOut(aggTempByStation, true)
}

func timeFuncCallElapsed(name string, runner OneBRCRunner, filename string) (map[string][onebrc.NumMetrics]int16, error) {
	time_now := time.Now()
	slog.Info(name, "start", time_now)
	res, err := runner.Run(filename)
	time_elapsed := time.Since(time_now)
	slog.Info(name, "time_elapsed", time_elapsed, "time_start", time_now, "time_end", time.Now())
	return res, err
}
