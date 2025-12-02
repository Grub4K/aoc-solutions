package y2025

import (
	"bufio"
	"io"
	"strconv"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

func day01(r io.Reader) aoc.Result {
	scanner := bufio.NewScanner(r)
	scanner.Split(bufio.ScanLines)

	dial := 50
	counterA := 0
	counterB := 0
	clockwise := true
	for scanner.Scan() {
		line := scanner.Text()
		value, err := strconv.ParseUint(line[1:], 10, 32)
		if err != nil {
			return aoc.Error(err)
		}
		movement := int(value)

		if line[0] == 'R' != clockwise {
			dial = (100 - dial) % 100
			clockwise = !clockwise
		}

		total := dial + movement
		counterB += total / 100
		dial = total % 100
		if dial == 0 {
			counterA++
		}
	}
	if err := scanner.Err(); err != nil {
		return aoc.Error(err)
	}

	return aoc.Solution(counterA, counterB)
}
