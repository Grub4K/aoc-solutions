package y2025

import (
	"bytes"
	"io"
	"slices"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

type d04 struct{}

func (d d04) run(r io.Reader) aoc.Result {
	const offset = 1 << 10
	buf := make([]byte, 0, 1<<17)

	w := bytes.NewBuffer(buf)
	w.Write(buf[:offset])
	n, err := io.Copy(w, r)
	if err != nil {
		return aoc.Error(err)
	}

	lineLen := bytes.IndexByte(w.Bytes(), '\n') - offset
	w.Write(buf[:lineLen+2])
	buf = w.Bytes()

	d.replaceSymbols(buf[offset : offset+n])
	grid := buf[offset-lineLen-2 : offset+int(n)+lineLen+2]

	var totalA int
	grid, totalA = d.runIteration(grid, lineLen)

	totalB := totalA
	removed := totalA
	for removed > 0 {
		grid, removed = d.runIteration(grid, lineLen)
		totalB += removed
	}

	return aoc.Solution(totalA, totalB)
}

func (d04) runIteration(grid []byte, lineLen int) ([]byte, int) {
	newGrid := slices.Clone(grid)
	indices := [9]int{
		0, 1, 2,
		lineLen + 1, lineLen + 2, lineLen + 3,
		2 * (lineLen + 1), 2*(lineLen+1) + 1, 2*(lineLen+1) + 2,
	}

	total := 0
	for indices[8] < len(grid) {
		for range lineLen {
			if grid[indices[4]] == 1 {
				surrounding := 0 +
					grid[indices[0]] + grid[indices[1]] + grid[indices[2]] +
					grid[indices[3]] + grid[indices[5]] +
					grid[indices[6]] + grid[indices[7]] + grid[indices[8]]
				if surrounding < 4 {
					newGrid[indices[4]] = 0
					total++
				}
			}

			for i := range indices {
				indices[i]++
			}
		}
		for i := range indices {
			indices[i]++
		}
	}
	return newGrid, total
}

func (d04) replaceSymbols(grid []byte) {
	for i, value := range grid {
		switch value {
		case '\n', '.':
			grid[i] = 0
		case '@':
			grid[i] = 1
		}
	}
}
