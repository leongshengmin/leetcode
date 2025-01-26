package main

import (
	"log/slog"
	"main/onebrc"
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
	Run(filename string) (map[string]string, error)
}

// max, min, sum, count
const filePath = "/Users/leongshengmin/Documents/leetcode/onebrc/1brc/data/weather_stations.csv"

func main() {
	// a1 := onebrc.Attempt1{}
	a2 := onebrc.Attempt2{}
	aggTempByStation, err := a2.Run(filePath)
	if err != nil {
		slog.Error("failed to run benchmark", "err", err)
		return
	}

	onebrc.OutputResultToStdOut(aggTempByStation)
}
