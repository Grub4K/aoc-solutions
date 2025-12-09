package y2025

import (
	"github.com/Grub4K/aoc-solutions/go/aoc"
)

var Days = map[uint8]aoc.Solver{
	1: day01,
	2: day02,
	3: d03{}.run,
	4: d04{}.run,
	6: d06{}.run,
	7: d07{}.run,
	8: d08{}.run,
}
