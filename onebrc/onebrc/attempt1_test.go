package onebrc

import (
	"log/slog"
	"os"
	"testing"
)

const testFilePath = "/Users/leongshengmin/Documents/leetcode/onebrc/testdata/sample.txt"
const numStations = 35


func TestAggregateByStation(t *testing.T) {
	_, err := os.Stat(testFilePath)
	if err != nil {
		t.Fatalf("Failed to stat %s: %v", testFilePath, err)
	}
	a1 := Attempt1{}
	expectedAggResults := map[string][NumMetrics]int16{
		"Tom Price": {
			263,
			-268,
			257,
			3,
		},
		"Kawachinagano": {
			-764,
			-764,
			-764,
			1,
		},
		"La Flèche": {
			747,
			747,
			747,
			1,
		},
	}
	aggTempByStation, err := a1.Run(testFilePath)
	if err != nil {
		slog.Error("failed to run benchmark", "err", err)
		return
	}
	if len(aggTempByStation) != numStations {
		t.Errorf("expected %d stations, got %d", numStations, len(aggTempByStation))
	}
	// max, min, sum, count
	for station, metrics := range aggTempByStation {
		expectedMetrics, ok := expectedAggResults[station]
		if !ok {
			continue
		}
		for i, metric := range metrics {
			if metric != expectedMetrics[i] {
				t.Errorf("station=%s, expected metric %d to be %d, got %d", station, i, expectedMetrics[i], metric)
			}
		}
	}
}
