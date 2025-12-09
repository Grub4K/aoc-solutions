package y2025

import (
	"bufio"
	"cmp"
	"io"
	"math"
	"slices"
	"strconv"
	"strings"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

type d08Vector3 struct {
	X, Y, Z uint64
}

func (v *d08Vector3) Dist(other d08Vector3) float64 {
	dx := v.X - other.X
	dy := v.Y - other.Y
	dz := v.Z - other.Z
	return math.Sqrt(float64(dx*dx + dy*dy + dz*dz))
}

type d08Dist struct {
	Dist float64
	A, B d08Vector3
}

type d08 struct{}

func (d d08) run(r io.Reader) aoc.Result {
	points, err := d.parse(r)
	if err != nil {
		return aoc.Error(err)
	}

	var dists []*d08Dist
	for i, point := range points {
		for _, other := range points[i+1:] {
			dists = append(dists, &d08Dist{
				Dist: point.Dist(other),
				A:    point,
				B:    other,
			})
		}
	}
	slices.SortFunc(dists, func(a, b *d08Dist) int {
		return cmp.Compare(a.Dist, b.Dist)
	})

	var resultA int
	var resultB uint64

	index := 0
	conns := 0
	groupCount := 0
	groups := map[d08Vector3]int{}
	for _, dist := range dists {
		// part a
		if conns == 1000 {
			conns = -1
			counts := make([]int, index)
			for _, group := range groups {
				counts[group-1] += 1
			}
			slices.SortFunc(counts, func(a, b int) int {
				return b - a
			})
			resultA = 1
			for _, count := range counts[:3] {
				resultA *= count
			}
		} else {
			conns += 1
		}

		aGroup := groups[dist.A]
		bGroup := groups[dist.B]
		switch {
		case aGroup == 0 && bGroup == 0:
			index++
			groupCount += 1
			groups[dist.A] = index
			groups[dist.B] = index

		case aGroup == 0:
			groups[dist.A] = bGroup

		case bGroup == 0:
			groups[dist.B] = aGroup

		case aGroup != bGroup:
			groupCount -= 1
			for key, group := range groups {
				if group == bGroup {
					groups[key] = aGroup
				}
			}

		default:
			continue
		}

		// part b
		if groupCount == 1 && len(groups) == len(points) {
			resultB = dist.A.X * dist.B.X
			break
		}
	}

	return aoc.Solution(resultA, resultB)
}
func (d d08) parse(r io.Reader) ([]d08Vector3, error) {
	var points []d08Vector3

	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		line := scanner.Text()
		a, after, found := strings.Cut(line, ",")
		if !found {
			continue
		}
		b, c, found := strings.Cut(after, ",")
		if !found {
			continue
		}
		x, err := strconv.ParseUint(a, 10, 64)
		if err != nil {
			return nil, err
		}
		y, err := strconv.ParseUint(b, 10, 64)
		if err != nil {
			return nil, err
		}
		z, err := strconv.ParseUint(c, 10, 64)
		if err != nil {
			return nil, err
		}
		points = append(points, d08Vector3{
			X: x,
			Y: y,
			Z: z,
		})
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return points, nil
}
