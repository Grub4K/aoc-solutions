package y2025

import (
	"bytes"
	"io"
	"strconv"
	"strings"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

func day02(r io.Reader) aoc.Result {
	l, err := io.ReadAll(r)
	if err != nil {
		return aoc.Error(err)
	}
	line := strings.TrimSpace(string(l))

	var buf [32]byte

	counterA := uint64(0)
	counterB := uint64(0)
	for r := range strings.SplitSeq(line, ",") {
		s, e, _ := strings.Cut(r, "-")
		start, err := strconv.ParseUint(s, 10, 64)
		if err != nil {
			return aoc.Error(err)
		}
		end, err := strconv.ParseUint(e, 10, 64)
		if err != nil {
			return aoc.Error(err)
		}

		for numEnc := start; numEnc <= end; numEnc++ {
			num := strconv.AppendUint(buf[:0:32], numEnc, 10)
			length := len(num) / 2
			// Part 1
			if bytes.Equal(num[:length], num[length:]) {
				counterA += numEnc
			}

			// Part 2
		nextSize:
			for ; length > 0; length-- {
				if len(num)%length != 0 {
					continue
				}
				control := num[0:length]
				for offset := length; offset < len(num); offset += length {
					part := num[offset : offset+length]
					if !bytes.Equal(part, control) {
						continue nextSize
					}
				}
				counterB += numEnc
				break
			}
		}
	}

	return aoc.Solution(counterA, counterB)
}
