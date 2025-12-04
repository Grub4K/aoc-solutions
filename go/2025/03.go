package y2025

import (
	"bufio"
	"io"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

type d03 struct{}

func (d d03) run(r io.Reader) aoc.Result {
	totalA := 0
	totalB := 0
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		line := scanner.Bytes()
		totalA += d.processLine(line, 2)
		totalB += d.processLine(line, 12)
	}
	if err := scanner.Err(); err != nil {
		return aoc.Error(err)
	}
	return aoc.Solution(totalA, totalB)
}

func (d03) processLine(line []byte, size int) int {
	total := 0

	start := 0
	end := len(line) - size
	for range size {
		end++
		offset := 0
		highest := byte(0)
		for i, v := range line[start:end] {
			value := v - '0'
			if value > highest {
				highest = value
				offset = i
			}

			if highest == 9 {
				break
			}
		}
		start += offset + 1
		total = 10*total + int(highest)
	}

	return total
}
