package main

import (
	y2021 "github.com/Grub4K/aoc-solutions/go/2021"
	y2025 "github.com/Grub4K/aoc-solutions/go/2025"
	"github.com/Grub4K/aoc-solutions/go/aoc"
)

var Years = map[uint16]map[uint8]aoc.Solver{
	2021: y2021.Days,
	2025: y2025.Days,
}
