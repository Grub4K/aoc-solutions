package y2021

import (
	"bytes"
	"io"
	"strconv"
	"strings"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

func day06(r io.Reader) aoc.Result {
	fish := [9]uint64{}

	data, err := io.ReadAll(r)
	if err != nil {
		return aoc.Error(err)
	}
	data = bytes.TrimSpace(data)

	for i := range strings.SplitSeq(string(data), ",") {
		index, err := strconv.ParseUint(i, 10, 8)
		if err != nil {
			return aoc.Error(err)
		}
		fish[index]++
	}

	from := 0
	to := 7

	for range 80 {
		fish[to] += fish[from]
		to = (to + 1) % 9
		from = (from + 1) % 9
	}

	a := uint64(0)
	for i := range 9 {
		a += fish[i]
	}

	for range 256 - 80 {
		fish[to] += fish[from]
		to = (to + 1) % 9
		from = (from + 1) % 9
	}

	b := uint64(0)
	for i := range 9 {
		b += fish[i]
	}

	return aoc.Solution(a, b)
}
