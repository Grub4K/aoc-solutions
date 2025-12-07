package y2025

import (
	"bufio"
	"bytes"
	"io"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

type d07 struct{}

func (d d07) run(r io.Reader) aoc.Result {
	scanner := bufio.NewScanner(r)
	scanner.Scan()
	if err := scanner.Err(); err != nil {
		return aoc.Error(err)
	}
	initial := scanner.Bytes()

	columns := map[int]int{
		bytes.IndexAny(initial, "S"): 1,
	}

	resultA := 0
	for scanner.Scan() {
		line := scanner.Bytes()
		if len(line) == 0 {
			continue
		}

		newCols := map[int]int{}
		for column, amount := range columns {
			if line[column] == '^' {
				resultA += 1
				delete(columns, column)
				newCols[column-1] += amount
				newCols[column+1] += amount
			}
		}

		for col, amount := range newCols {
			columns[col] += amount
		}
	}
	if err := scanner.Err(); err != nil {
		return aoc.Error(err)
	}

	resultB := 0
	for _, amount := range columns {
		resultB += amount
	}
	return aoc.Solution(resultA, resultB)
}
