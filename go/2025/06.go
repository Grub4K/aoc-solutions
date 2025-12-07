package y2025

import (
	"io"
	"strconv"
	"strings"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

type d06 struct{}

func (d d06) run(r io.Reader) aoc.Result {
	data, err := io.ReadAll(r)
	if err != nil {
		return aoc.Error(err)
	}

	lines := strings.Split(string(data), "\n")
	if lines[len(lines)-1] == "" {
		lines = lines[:len(lines)-1]
	}
	length := len(lines[0])
	for _, line := range lines[1:] {
		if len(line) != length {
			return aoc.StrError("length of lines is not identical")
		}
	}

	var columns [][]string
	offset := 0
	index := 0
	for index < length {
		isSpace := true
		for _, line := range lines {
			if line[index] != ' ' {
				isSpace = false
			}
		}

		if isSpace {
			column := make([]string, len(lines))
			for i, line := range lines {
				column[i] = line[offset:index]
			}
			columns = append(columns, column)
			index++
			offset = index
		}
		index++
	}
	column := make([]string, len(lines))
	for i, line := range lines {
		column[i] = line[offset:index]
	}
	columns = append(columns, column)

	var resultA uint64
	var resultB uint64
	for _, column := range columns {
		op := column[len(column)-1]
		nums := column[:len(column)-1]

		result, err := d.solve(op, nums)
		if err != nil {
			return aoc.Error(err)
		}
		resultA += result

		cephalopodNums := make([]string, len(nums[0]))
		for i := range cephalopodNums {
			s := make([]byte, len(nums))
			for j, num := range nums {
				s[j] = num[i]
			}
			cephalopodNums[i] = string(s)
		}

		result, err = d.solve(op, cephalopodNums)
		if err != nil {
			return aoc.Error(err)
		}
		resultB += result
	}

	return aoc.Solution(resultA, resultB)
}

func (d06) solve(op string, nums []string) (uint64, error) {
	add := strings.ContainsAny(op, "+")

	result := uint64(0)
	if !add {
		result = 1
	}
	for _, num := range nums {
		n, err := strconv.ParseUint(strings.TrimSpace(num), 10, 64)
		if err != nil {
			return 0, err
		}
		if add {
			result = result + n
		} else {
			result = result * n
		}
	}

	return result, nil
}
